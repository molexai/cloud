from setuptools import setup, find_packages

setup(
    name="mlx-cloud",
    version="0.1.0",
    description="molexCloud, autonomous cloud manager",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="molexAI",
    author_email="mioisdeveloper@gmail.com",
    url="https://github.com/molexai/cloud",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
