from setuptools import setup, find_packages

long_description = """**rolling** is a collection of computationally efficient
rolling window iterators for Python.

Many useful arithmetical, logical and statistical functions are implemented
to allow the window to be computed in sub-linear time (and in many instances
constant time):

- Sum
- All
- Any
- Min
- Max
- Mean
- Median
- Variance
- Standard deviation

There's also a more general 'apply' mode where any specific function can be
applied to the window. Both fixed-length and variable-length windows are supported.
"""

setup(
    name='rolling',
    version='0.1.1',
    description='Efficient rolling window algorithms',
    long_description=long_description,
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
    ],
    keywords='rolling window iterator algorithms',
    project_urls={
      'Source': 'https://github.com/ajcr/rolling/',
      'Tracker': 'https://github.com/ajcr/rolling/issues',
    },
    python_requires='>=3.4.0',
    author='Alex Riley',
    license='MIT',
    packages=find_packages(),
    tests_require=['pytest>=2.8.0'],
    zip_safe=False,
)
