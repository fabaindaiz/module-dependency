from distutils.core import setup

# Getting requirements:
with open("requirements.txt") as requirements_file:
    requirements = requirements_file.readlines()

setup(
    name='module-injection',
    version='0.1',
    description='Python Module Injection',
    author='Fabian Diaz',
    author_email='github.clapping767@passmail.net',
    url='https://github.com/fabaindaiz/module-injection',
    packages=[
        'dependency'
    ],
    package_dir={
        "": "src",
    },
    install_requires=requirements
)