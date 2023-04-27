from setuptools import setup, find_packages

setup(
    name='image-tool',
    version='0.1',
    author='kk',
    author_email='',
    description='tool for image',
    packages=find_packages(),
    install_requires=[
        'rembg',
        'rembg[gpu]',
        'pillow'
    ],
)
