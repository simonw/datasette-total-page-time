from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-total-page-time",
    description="Add a note to the Datasette footer measuring the total page load time",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-total-page-time",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-total-page-time/issues",
        "CI": "https://github.com/simonw/datasette-total-page-time/actions",
        "Changelog": "https://github.com/simonw/datasette-total-page-time/releases",
    },
    license="Apache License, Version 2.0",
    classifiers=[
        "Framework :: Datasette",
        "License :: OSI Approved :: Apache Software License",
    ],
    version=VERSION,
    packages=["datasette_total_page_time"],
    entry_points={"datasette": ["total_page_time = datasette_total_page_time"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio"]},
    python_requires=">=3.7",
)
