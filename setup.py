from setuptools import setup, find_packages

setup(
    name="dati-moody",
    version="0.1",
    packages=find_packages(include=["utils", "utils.*"]),  # Only install utils
)
