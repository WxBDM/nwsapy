
import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

version = "1.0.3"

setup(
  name = 'nwsapy',         # How you named your package folder (MyLib)
  packages = find_packages(),   # Chose the same as "name"
  long_description=README,
  long_description_content_type="text/markdown",
  version = version,      # Start with a small number and increase it with every change you make
  license='apache-2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A pythonic implementation of the National Weather Service API',   # Give a short description about your library
  author = 'Brandon Molyneaux',                   # Type in your name
  email = 'bran.moly@gmail.com',
  url = 'https://github.com/WxBDM/nwsapy',   # Provide either the link to your github or to your website
  download_url = f'https://github.com/WxBDM/nwsapy/archive/refs/tags/v{version}.tar.gz',    # I explain this later on
  keywords = ['national weather service', 'nws', 'nws api'],   # Keywords that define your package best
  install_requires=[        # dependencies requried for the package.
          'shapely>=1.7.1',
          'pandas>=1.2.4',
          'numpy>=1.20.3',
          'pint>=0.17',
          'requests>=2.25.1'
      ],
  python_requires = '>=3.8',
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
