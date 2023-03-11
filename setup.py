from setuptools import setup, find_packages

from rolling import __version__

long_description = """**rolling** is a collection of computationally efficient
rolling window iterators for Python.

Many useful arithmetical, logical and statistical functions are implemented
to allow the window to be computed in sub-linear time (and in many instances
constant time). These include:

- Sum
- Min and Max
- All and Any
- Mean, Median and Mode
- Variance and Standard deviation

There's also a more general 'apply' mode where any specific function can be
applied to the window. Both fixed-length and variable-length windows are supported.
"""

setup(
    name='rolling',
    version=__version__,
    description='Efficient rolling window algorithms',
    long_description=long_description,
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      'Programming Language :: Python :: 3.10',
      'Programming Language :: Python :: 3.11',
    ],
    keywords='rolling window iterator algorithms',
    project_urls={
      'Source': 'https://github.com/ajcr/rolling/',
      'Tracker': 'https://github.com/ajcr/rolling/issues',
    },
    python_requires='>=3.7.0',
    author='Alex Riley',
    license='MIT',
    packages=find_packages(include=["rolling", "rolling.*"]),
    tests_require=['pytest>=2.8.0'],
    zip_safe=False,
)
