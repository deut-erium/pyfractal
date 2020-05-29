import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfractal-deut-erium", 
    version="0.0.2",
    author="Himanshu Sheoran",
    author_email="himanshuthesheoran@gmail.com",
    description="A GUI based fractal generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deut-erium/pyfractal",
    packages=setuptools.find_packages(),
    keywords="fractal GUI fractals gui",
    license = "MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    install_requires=['Pillow','tk','canvasvg'],
    python_requires='>=3.6',
)
