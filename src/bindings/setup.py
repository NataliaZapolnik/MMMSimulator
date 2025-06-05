from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "cpp_backend",  # Module name
        ["cpp_backend.cpp"],  # Source file(s)
        # Optional: extra_compile_args=["-O3"],  # For optimization
    ),
]

setup(
    name="cpp_backend",
    version="0.1",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)