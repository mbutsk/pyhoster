from setuptools import setup

setup(
    name="pyserve",
    version="0.1",
    packages=["pyserve"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pyserve=pyserve.main:start"
        ]
    },
)
