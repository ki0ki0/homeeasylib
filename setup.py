import setuptools

import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setuptools.setup(
  name="homeeasy",
  version=get_version("homeeasy/__init__.py"),
  description="Control HVAC devices compatible with HomeEasy application.",
  long_description=read("README.md"),
  long_description_content_type="text/markdown",
  url="https://github.com/ki0ki0/homeeasylib",
  author="Ihor Kostiuk",
  author_email="igorkost@gmail.com",
  license="GPLv3",
  packages=setuptools.find_packages(),
  install_requires=["paho-mqtt", "pycryptodome"],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Development Status :: 3 - Alpha",
    "Framework :: AsyncIO"
  ],
  python_requires='>=3.6',
)