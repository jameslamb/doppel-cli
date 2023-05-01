import os
from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as f:
    readme = f.read()

with open(os.path.join("doppel", "VERSION"), "r") as f:
    version = f.read().strip()

setup(
    name="doppel-cli",
    packages=find_packages(),
    description=(
        "An integration testing framework for testing API similarity of software libraries."
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords="api library testing CI",
    version=version,
    url="http://github.com/jameslamb/doppel-cli",
    project_urls={
        "Documentation": "https://doppel-cli.readthedocs.io/en/latest/",
        "Source": "http://github.com/jameslamb/doppel-cli",
        "Issue Tracker": "http://github.com/jameslamb/doppel-cli/issues",
    },
    license="BSD 3-clause",
    maintainer="James Lamb",
    maintainer_email="jaylamb20@gmail.com",
    install_requires=["click", "tabulate"],
    python_requires=">=3.8",
    package_data={"doppel": ["bin/analyze.R", "bin/analyze.py", "VERSION", "LICENSE"]},
    entry_points={
        "console_scripts": [
            "doppel-describe = doppel.describe:main",
            "doppel-test = doppel.cli:main",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Testing",
    ],
)
