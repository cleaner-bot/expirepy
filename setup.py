from setuptools import find_namespace_packages, setup  # type: ignore

setup(
    name="expirepy",
    version="0.1.0",
    url="https://github.com/cleaner-bot/expire.py",
    author="Leo Developer",
    author_email="git@leodev.xyz",
    description="Expire.py",
    packages=find_namespace_packages(include=["expirepy*"]),
    package_data={"expirepy": ["py.typed"]},
)
