try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='karcher-home',
    packages=['karcher'],
    include_package_data=True,
    version='0.2',
    license='MIT',
    description='Kärcher Home Robots client',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Lauris BH',
    author_email='lauris@nix.lv',
    url='https://github.com/lafriks/python-karcher',
    download_url='https://github.com/lafriks/python-karcher/releases/download/v0.1.1/karcher-home-0.1.1.tar.gz',
    platforms='any',
    install_requires=[
        'requests',
        'tzlocal',
        'click',
        'pycryptodome',
        'protobuf'
    ],
    entry_points='''
        [console_scripts]
        karcher-home=karcher.cli:safe_cli
    ''',
)
