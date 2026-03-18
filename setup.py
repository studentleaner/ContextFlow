from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="contextflow",
    version="0.1.0",
    description="A lightweight, deterministic Python library for Context Engineering.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="studentleaner",
    packages=find_packages(),
    install_requires=[
        "tiktoken>=0.7.0",
        "openai>=1.0.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0"
    ],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
