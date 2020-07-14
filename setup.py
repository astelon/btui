import sys
from setuptools import setup


if sys.version_info < (3, 0):
    sys.stderr.write("Sorry, Python < 3.0 is not supported\n")
    sys.exit(1)


setup(name='btui',
      version='0.0.1',
      description="""TUI library.""",
      long_description=open('README.md').read(),
      url='https://github.com/astelon/btui',
      author='Astelon',
      author_email='lg.marinblanco@gmail.com',
      license='LGPL',
      packages=['btui'])
