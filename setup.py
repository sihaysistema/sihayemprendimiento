from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sihayemprendimiento/__init__.py
from sihayemprendimiento import __version__ as version

setup(
	name="sihayemprendimiento",
	version=version,
	description="Si Hay Emprendimiento",
	author="Si Hay Sistema",
	author_email="m.m@sihaysistema.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
