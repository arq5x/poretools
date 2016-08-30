import os
from setuptools import setup

version_py = os.path.join(os.path.dirname(__file__), 'poretools', 'version.py')
version = open(version_py).read().strip().split('=')[-1].replace('"','').strip()
print version
long_description = """
``poretools`` is a toolset for working with nanopore sequencing data'
"""

HERE = os.path.dirname(__file__)

with open(os.path.join(HERE, "requirements.txt"), "r") as f:
    install_requires = [x.strip() for x in f.readlines()]

setup(
    name="poretools",
    version=version,
    install_requires=install_requires,
    requires=['python (>=2.7, <3.0)'],
    packages=['poretools',
              'poretools.scripts'],
    author="Nick Loman and Aaron Quinlan",
    description='A toolset for working with nanopore sequencing data',
    long_description=long_description,
    url="http://poretools.readthedocs.org",
    package_dir={'poretools': "poretools"},
    package_data={'poretools': []},
    zip_safe=False,
    include_package_data=True,
    #scripts=['poretools/scripts/poretools'],
    entry_points={
        'console_scripts': [
            'poretools=poretools.poretools_main:main',
        ],
    },
    author_email="arq5x@virginia.edu",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
        ]
    )
