from setuptools import setup, find_packages

setup(
    name="zadaniator_backend",
    version="0.4",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django",
        "gunicorn"
    ],
)