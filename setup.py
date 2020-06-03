import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfractal", 
    version="0.0.2",
    author="Himanshu Sheoran",
    author_email="himanshuthesheoran@gmail.com",
    description="A GUI based fractal generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deut-erium/pyfractal",
    packages=setuptools.find_packages(),
    include_package_data=True,
    keywords="fractal GUI graphics turtle beautiful",
    license = "MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    install_requires=['Pillow>=7.0.0','tk>=0.0.1','canvasvg>=1.0.0'],
    python_requires='>=3.5',
)
