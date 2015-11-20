
from setuptools import setup, find_packages
from os import walk
from os.path import join, dirname, sep
import os
import glob

# NOTE: All package data should also be set in MANIFEST.in

packages = find_packages()

package_data = {'': ['*.tmpl',
                     '*.patch', ], }

data_files = []

# By specifying every file manually, package_data will be able to
# include them in binary distributions. Note that we have to add
# everything as a 'pythonforandroid' rule, using '' apparently doesn't
# work.
def recursively_include(results, directory, patterns):
    for root, subfolders, files in walk(directory):
        for fn in files:
            if not any([glob.fnmatch.fnmatch(fn, pattern) for pattern in patterns]):
                continue
            filename = join(root, fn)
            directory = 'pythonforandroid'
            if directory not in results:
                results[directory] = []
            results[directory].append(join(*filename.split(sep)[1:]))

recursively_include(package_data, 'vispytopovray/templates',
                    ['*.tmpl'])

setup(name='vispytopovray',
      version='0.1',
      description='Vispy scene to POV-Ray .pov file exporter',
      author='Alexander Taylor',
      author_email='alexanderjohntaylor@gmail.com',
      url='https://github.com/inclement/vispy-to-povray', 
      license='GPL', 
      install_requires=[],
      classifiers = [
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: OS Independent',
          'Operating System :: POSIX :: Linux',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities',
          ],
      packages=packages,
      package_data=package_data,
      )
