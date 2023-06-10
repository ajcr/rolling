# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.5.0]
### Added
- New `rolling.ApplyPairwise` object.
- Add `"indexed"` window type to enable operations on windows over `(index, value)` pairs (initial implementation work by @daviddavo)

## [0.4.0] - 2023-03-11
### Added
- `__version__` attribute added to package
- New `rolling.PolynomialHash()` object
- New `rolling.Match()` object
- New `rolling.Monotonic()` object

### Changed
- test modules no longer included pip install
- faster rolling median implementation using SortedList
- Entropy supports relative entropy computation by passing reference distribution.
- Entropy supports base argument to change base of logarithm.

## [0.3.0] - 2021-11-24
### Added
- extend() method added to rolling objects

### Changed
- support Python 3.6 to 3.9, remove support for earlier versions
- Use tuples instead of namedtuples in the `minmax` module for increased performance
- Correct Std/Var calculation when difference between sum of squared values and mean is negative.

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
