from setuptools import setup

setup(
    name='rolling',
    version='0.1',
    description='Efficient rolling window algorithms',
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
    packages=['rolling'],
    tests_require=['pytest>=2.8.0'],
    zip_safe=False,
)
