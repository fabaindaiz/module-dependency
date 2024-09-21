import sys

from distutils.core import setup

def _open(filename):
    if sys.version_info[0] == 2:
        return open(filename)
    return open(filename, encoding="utf-8")

# Getting requirements:
with _open("requirements.txt") as requirements_file:
    requirements = requirements_file.readlines()


setup(name='dependency-module',
      version='0.1',
      description='Python Dependency Module',
      author='Fabian Diaz',
      author_email='github.clapping767@passmail.net',
      url='https://github.com/fabaindaiz/python-dependency-module/',
      packages=[
          'dependency'
      ],
      package_dir={
          "": "src",
      },
      install_requires=requirements
     )