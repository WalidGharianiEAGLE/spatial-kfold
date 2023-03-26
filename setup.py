import pathlib
from setuptools import setup, find_packages

# The directory containing this file
dir = pathlib.Path(__file__).parent

# README file
README = (dir / "README.md").read_text()

# Dependencies
with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='spatial-kfold',
    version="0.0.01",
    packages=["spatialkfold"],
    author="Walid Ghariani",
    author_email="walid11ghariani@gmail.com",
    description=("spatial-kfold: A Python Package for Spatial Resampling Toward More Reliable Cross-Validation in Spatial Studies."),
    long_description=README,
    license="MIT",
    keywords="cross-validation, machine-learning, GIS, spatial",
    url="https://github.com/WalidGharianiEAGLE/spatial-kfold",

    #packages=find_packages(),
    package_data={'geopoz': ['./data/*.geojson']},
    include_package_data=True,

    # Dependencies
    install_requires = requirements,
    python_requires='>=3.7',
 
    # Classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    # testing
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)