import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="homeeasy",
  version="0.0.2",
  description="Control HVAC devices compatible with HomeEasy application.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ki0ki0/homeeasylib",
  author="Ihor Kostiuk",
  author_email="igorkost@gmail.com",
  license="GPLv3",
  packages=setuptools.find_packages(),
  install_requires=["paho-mqtt", "pycryptodome", "structlog"],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Development Status :: 3 - Alpha",
    "Framework :: AsyncIO"
  ],
  python_requires='>=3.6',
)