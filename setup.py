from setuptools import setup, find_packages

setup(
    name="MyUtilities",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "parse", 
    ],
    author="MattThePerson",
    description="Various utility functions and classes of mine.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
