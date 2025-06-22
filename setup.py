import pathlib
from setuptools import setup

dir = pathlib.Path(__file__).parent
README = (dir / "README.md").read_text()
# Dependencies
with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name="spatial-kfold",
    version="0.0.4",
    packages=["spatialkfold"],
    author="Walid Ghariani",
    author_email="walid11ghariani@gmail.com",
    description=(
        "spatial-kfold: A Python Package for Spatial Resampling Toward More Reliable Cross-Validation in Spatial Studies."
    ),
    long_description=README,
    long_description_content_type="text/markdown",
    license="GPL-3.0",
    keywords="cross-validation, machine-learning, GIS, spatial",
    url="https://github.com/WalidGharianiEAGLE/spatial-kfold",
    package_data={"spatialkfold": ["./data/*.geojson"]},
    include_package_data=True,
    # Dependencies
    install_requires=requirements,
    python_requires=">=3.7",
    # Classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    # testing
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
