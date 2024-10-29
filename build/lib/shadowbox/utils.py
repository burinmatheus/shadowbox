import tempfile
import tarfile
import os

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