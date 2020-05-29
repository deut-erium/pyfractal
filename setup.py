import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfractal-deut-erium", # Replace with your own username
    version="0.0.1",
    author="Himanshu Sheoran",
    author_email="himanshuthesheoran@gmail.com",
    description="A GUI based fractal generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
