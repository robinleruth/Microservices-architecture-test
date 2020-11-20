from setuptools import setup, find_packages

setup(
    name='tcommon',
    version='1.0',
    description='Functions that will need to be used by different services',
    author='Robin',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'requests',
        'aioredis',
        'asyncio'
    ]
)
