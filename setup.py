import os
from setuptools import setup, find_packages

setup(
    name="catgirl-downloader",
    version="1.1.0",
    description="GTK4/PyGObject anime image downloader with multi-source support including yande.re",
    author="CatgirlDownloader Contributors",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "PyGObject>=3.40.0",
    ],
    data_files=[
        ('share/applications', ['data/io.github.catgirldownloader.desktop']),
    ],
    entry_points={
        "console_scripts": [
            "catgirl-downloader=catgirl_downloader.cli:main",
            "catgirl-downloader-gui=catgirl_downloader.gui.app:main",
        ],
    },
    python_requires=">=3.8",
)
