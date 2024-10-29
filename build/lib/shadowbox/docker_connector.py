from docker import DockerClient

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