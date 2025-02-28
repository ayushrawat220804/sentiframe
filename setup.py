from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sentiframe",
    version="0.1.0",
    author="Ayush Rawat",
    author_email="ayushrawat220804@gmail.com",
    description="A flexible framework for scraping and analyzing YouTube comments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ayushrawat220804/sentiframe",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "google-api-python-client>=2.108.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "web": ["streamlit>=1.29.0"],
    },
) 