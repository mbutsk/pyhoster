from setuptools import setup

setup(
    name="pyserve",
    version="1.0.0",
    packages=["pyserve"],
    install_requires=["psutil"],
    entry_points={
        "console_scripts": [
            "pyserve=pyserve.main:launch"
        ]
    },
    data_files = [('share/man/man8', ['pyserve.8'])],
)
