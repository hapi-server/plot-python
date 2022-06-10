import sys
from setuptools import setup, find_packages

#install_requires = ["matplotlib", "hapiclient @ git+https://github.com/hapi-server/client-python#egg=hapiclient"]
install_requires = ["matplotlib", "hapiclient>0.1.7"]

if len(sys.argv) > 1 and sys.argv[1] == 'develop':
    install_requires.append("deepdiff<3.3.0")
    install_requires.append("pillow")
    print(sys.version_info)
    if sys.version_info < (3, 6):
        install_requires.append("pytest<5.0.0")
    elif sys.version_info < (3, 7):
        install_requires.append("pytest<7.0.0")
    else:
        # Should not be needed, as per
        # https://docs.pytest.org/en/stable/py27-py34-deprecation.html
        # Perhaps old version of pip causes this?
        install_requires.append("pytest")

# version is modified by misc/version.py (executed from Makefile). Do not edit.
setup(
    name='hapiplot',
    version='0.2.1',
    author='Bob Weigel',
    author_email='rweigel@gmu.edu',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/hapiplot/',
    license='LICENSE.txt',
    description='Plot data from HAPI server',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=install_requires
)