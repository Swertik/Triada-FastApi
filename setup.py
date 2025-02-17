import setuptools
import os


setuptools.setup(
    name="triada",
    version="0.1.1",
    author="Swertik",
    author_email="herobrine664@gmail.com",
    description="Triada",
    packages=setuptools.find_packages(),
    install_requires=[
        "annotated-types==0.7.0",
        "anyio==4.8.0",
        "certifi==2024.12.14",
        "fastapi==0.115.8",
        "h11==0.14.0",
        "httpcore==1.0.7",
        "httpx==0.28.1",
        "idna==3.10",
        "psycopg2==2.9.10",
        "pydantic==2.10.6",
        "pydantic_core==2.27.2",
        "sniffio==1.3.1",
        "starlette==0.45.3",
        "typing_extensions==4.12.2"
    ]
)