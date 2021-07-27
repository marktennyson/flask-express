from setuptools import setup,find_packages


VERSION = "0.0.3"
AUTHOR = "Aniket Sarkar"

with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="Flaske",
    version=VERSION,
    url="https://github.com/marktennyson/flaske",
    license="GNU General Public License v3 or later (GPLv3+)",
    author=AUTHOR,
    author_email="aniketsarkar@yahoo.com",
    description="interactive app like expressJs for flask.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["flask", "flaske", "Navycut"],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=[ 
        "asgiref==3.4.1",
        "click==8.0.1",
        "Flask==2.0.1",
        "itsdangerous==2.0.1",
        "Jinja2==3.0.1",
        "MarkupSafe==2.0.1",
        "munch==2.5.0",
        "six==1.16.0",
        "Werkzeug==2.0.1"
    ],
    extras_require={},
    python_requires=">=3.6,<4",

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)