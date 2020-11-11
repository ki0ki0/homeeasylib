import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
  name="homeeasy",
  version="0.0.1",
  description="Control HVAC devices compatible with HomeEasy application.",
  long_description=README,
  long_description_content_type="text/markdown",
  author="",
  author_email="",
  license="GPLv3",
  packages=["homeeasy"],
  install_requires=["paho-mqtt", "pycryptodome", "structlog"],
  zip_safe=False
)