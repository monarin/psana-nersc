#python setup.py build_ext --inplace

from distutils.core import setup, Extension
from Cython.Build import cythonize

setup(ext_modules = cythonize(Extension(
            "profdgram",                
            sources=["profdgram.pyx"],    
      ),
      compiler_directives={'language_level' : "3"}
      ))
