import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup



import sys
if sys.version_info < (3, 4):
    sys.exit('Python 3.4 or greater is required.')

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup



with open('RELEASE') as f:
    lines = f.readlines()

version = lines[0]
version = version.strip().split()[-1]

VERSION = version

LICENSE = "MIT"


setup(
    name='Mmint',
    version=VERSION,
    description=(
        'Methylation data mining tools'
    ),
    long_description='',
    author='Jia Li',
    author_email='jiali@tamu.edu',
    maintainer='Deqiang Sun',
    maintainer_email='dsun@tamu.edu',
    license=LICENSE,
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/lijiacd985/Mmint',
    install_requires=[
        "matplotlib",
        "numpy",
        "pandas",
        "scikit-learn",
        "scipy",
        "seaborn",
        "pysam",
        "deepTools",
        "suds-py3",
        "pybedtools",
    ],
    scripts=[
        "mmint",
    ],
    include_package_data=True,
)
