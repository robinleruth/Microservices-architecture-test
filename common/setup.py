from setuptools import setup

setup(
    name='tcommon',
    version='1.0',
    description='Functions that will need to be used by different services',
    author='Robin',
    packages=["tcommon"],
    install_requires=[
        'fastapi',
        'requests'
    ]
)
