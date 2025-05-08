from setuptools import setup, find_packages

def readme():
    try:
        with open('pypi-description.md', 'r') as f:
            return f.read()
    except:
        return 'A simple tool for servers that host python projects'

setup(
    name="pyhoster",
    version="1.0.1",
    packages=find_packages(),
    install_requires=["psutil"],
    entry_points={
        "console_scripts": [
            "pyhoster=pyhoster.main:launch"
        ]
    },
    data_files = [('share/man/man8', ['pyhoster.8'])],
    description='A simple tool for servers that host python projects',
    author='mbutsk',
    author_email='mbutsk@icloud.com',
    url = "https://github.com/mbutsk/pyhoster",
    license="MIT License, see LICENSE.md file",
    long_description=readme(),
    long_description_content_type='text/markdown',
    keywords = [
        "cli",
        "server",
        "process",
        "manager",
        "console",
        "script"
    ],
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Operating System :: Unix",
        "Intended Audience :: System Administrators",
    ]
)
