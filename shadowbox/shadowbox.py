from docker import DockerClient
from uuid import uuid4
import os
import io
import tempfile
import tarfile

class ShadowBox():
    def __init__(self, ip, port):
        self.client = DockerConnector().get_connection(ip, port)

    def run(self, image_name, source_code, files, output_file_name, mem_limit='512m') -> str:
        name = 'shaddowbox-' + uuid4().hex
        container = None

        file_path = None
        tar_file_path = None

        try:
            file_path = Utils.create_temp_file_from_string(source_code.decode())
            tar_file_path = Utils.compress_file_to_tar(file_path)
            file_container_path = '/app/' + os.path.basename(file_path)

            container = self.client.containers.run(
                image=image_name, 
                working_dir='/app',
                mem_limit=mem_limit, 
                name=name, 
                network_disabled=True,
                network_mode='none', 
                read_only=False,
                detach=True,
                command=['tail', '-f', '/dev/null'],
            )
            
            with open(tar_file_path, 'rb') as tar_file:
                container.put_archive('/app', tar_file.read())

            for file in files:
                tar_aux_file_path = Utils.compress_file_to_tar(file)
                with open(tar_aux_file_path, 'rb') as tar_aux_file:
                    container.put_archive('/app', tar_aux_file.read())
                
                os.remove(tar_aux_file_path)

            container.exec_run(['chmod', '777', file_container_path])
            retorno = container.exec_run(['python3', file_container_path])
           
            if retorno.exit_code == 1:
                raise Exception("Não foi possível executar o código-fonte Python!\nDetalhes: " + str(retorno.output));

            compacted_file = container.get_archive('/app/' + output_file_name)
            
            response = Utils.decompress_tar_to_str(compacted_file[0])
            return response
        except Exception as e:
            print(f"Error: {e}")
            raise e;
        
        finally:
            if file_path:
                os.remove(file_path)
            if tar_file_path:
                os.remove(tar_file_path)

            if container:
                self.destroy(container)

    def stop(self, container):
        container.stop()
    
    def destroy(self, container):
        container.kill()
        container.remove()
    
    def list(self):
        return self.client.containers.list()
    
class DockerConnector:
    def get_connection(self, ip, port) -> DockerClient:
        if 'connection' not in self.__dict__:
            self.connection = DockerClient(
                    base_url='tcp://{}:{}'.format(ip, port), 
                    version='auto', 
                    timeout=10, 
                    tls=False
                )
            
        return self.connection

class Utils: 
    def create_temp_file_from_string(content: str) -> str:
        fd, temp_file = tempfile.mkstemp(suffix='.py')
        os.chmod(temp_file, 0o644)

        with os.fdopen(fd, 'w') as f:
            f.write(content)

        return temp_file

    def compress_file_to_tar(file_path: str) -> str:
        tar_file_path = file_path + '.tar.gz'

        with tarfile.open(tar_file_path, "w:gz") as tar:
            tar.add(file_path, arcname=os.path.basename(file_path))

        return tar_file_path
    
    def decompress_tar_to_str(archive_bits) -> str:
        file_data = io.BytesIO()
        for chunk in archive_bits:
            file_data.write(chunk)
        file_data.seek(0)

        with tarfile.open(fileobj=file_data, mode="r") as tar:
            for member in tar.getmembers():
                if member.isfile():
                    extracted_file = tar.extractfile(member)
                    if extracted_file:
                        return extracted_file.read().decode('utf-8')