from setuptools import setup, find_packages

setup(
    name='datastore_server',
    version="0.1.0",
    packages=find_packages(),
    scripts=['datastore_server.py'],
    package_data= {
        '' : ['*.txt']
    },
    install_requires=['googleclouddatastore==v1beta2-rev1-2.1.0'],
    author="Thomas Stephenson", 
    author_email='ovangle@gmail.com'
)

