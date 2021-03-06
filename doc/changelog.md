# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [Unreleased]
### Changed
- support Python 3.6 to 3.9, remove support for earlier versions

### Added
- extend() method added to rolling objects

## [0.2.0] - 2018-05-12
### Added
- Add this changelog to the doc directory
- Nunique class
- Add Mode class (supported by a BiCounter, a bi-directional counter)
- Add Entropy class (Shannon entropy, fixed-size windows only)
- Add Skew class (skewness)
- Add Kurtosis class

### Removed
- Remove general rolling() function


## [0.1.1] - 2018-03-01
### Changed
- Fix PyPI install errors
- Fix comments and docstrings on RollingBase
- Fix comments and docstrings on MinHeap
- Add long description to setup.py for PyPI
- Restructure directory so that tests are included for pip install

## [0.1.0] - 2018-02-28
### Added
- rolling released to PyPI
