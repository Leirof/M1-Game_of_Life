# several files with ext .pyx, that i will call by their name
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

ext_modules=[
    Extension("primes",       ["GameOfLife.py"]),
    Extension("spam",         ["GoL_utils.py"])
]

setup(
  name = 'Game of Life',
  cmdclass = {'build_ext': build_ext},
  ext_modules = cythonize(ext_modules, language_level = "3")
  
)