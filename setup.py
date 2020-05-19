#! /usr/bin/env python
#
# Copyright (C) 2020-2020 Victor Kharlamov

DESCRIPTION = "PrettyAnalyticPlots: special plots for analysis"

DISTNAME = "PrettyAnalyticPlots"
MAINTAINER = "Victor Kharlamov"
MAINTAINER_EMAIL = 'vi.kharlamov@gmail.com'
DOWNLOAD_URL = 'https://github.com/Xapulc/PrettyAnalyticPlots'
VERSION = '0.1.0'
PYTHON_REQUIRES = ">=3.6"

INSTALL_REQUIRES = [
    'numpy>=1.13.3',
    'scipy>=1.0.1',
    'pandas>=0.22.0',
    'matplotlib>=2.1.2',
]


PACKAGES = [
    'analyticplots'
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Multimedia :: Graphics',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Operating System :: MacOS'
]

if __name__ == "__main__":
    from setuptools import setup

    import sys

    if sys.version_info[:2] < (3, 6):
        raise RuntimeError("package requires python >= 3.6.")

    setup(
        name=DISTNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        version=VERSION,
        download_url=DOWNLOAD_URL,
        python_requires=PYTHON_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        packages=PACKAGES,
        classifiers=CLASSIFIERS
    )