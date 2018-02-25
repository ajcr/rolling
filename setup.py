from setuptools import setup

setup(name='rolling',
      version='0.1',
      description='Efficient rolling window algorithms',
      url='https://github.com/ajcr/rolling',
      python_requires='>=3.4.0',
      author='Alex Riley',
      license='MIT',
      packages=['rolling'],
      tests_require=['pytest>=2.8.0'],
      zip_safe=False)
