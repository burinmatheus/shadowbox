from setuptools import find_packages, setup

def load_requirements():
    with open("requirements.txt") as req:
        content = req.readlines()
    return [line.strip() for line in content]

setup(
    name='shadowbox',
    version='1.0',
    author="Matheus M. Burin",
    author_email="matheus@burinmatheus.dev",
    license = "MIT",
    keywords = "sandbox, security, AI, python, code, interpreter",
    description="A simple package to create a sandbox environment to run AI codes",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/burinmatheus/shadowbox",
    packages=find_packages(include=['shadowbox']),
    install_requires=load_requirements(), 
    python_requires=">=3.12",
    classifiers=[]
)