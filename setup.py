import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sagemaker-knockout",
    version="0.0.3",
    author="Mario Kostelac",
    author_email="mario.kostelac@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mariokostelac/sagemaker-knockout",
    packages=setuptools.find_packages(),
    install_requires=[
        "psutil",
        "gputil",
        "daemonize"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
