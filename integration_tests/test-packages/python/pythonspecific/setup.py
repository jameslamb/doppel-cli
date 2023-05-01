from setuptools import find_packages, setup

setup(
    name="pythonspecific",
    packages=find_packages(),
    description="""
    Test package used to check Python-specific
    things.
    """,
    version="0.0.1",
    maintainer="James Lamb",
    maintainer_email="jaylamb20@gmail.com",
    install_requires=[],
    extras_require={},
)
