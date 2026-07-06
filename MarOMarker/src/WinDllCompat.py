"""
Windows DLL compatibility helper.

The PyQt5 Qt wheel bundles outdated MSVC runtime DLLs. If Qt loads them
before TensorFlow is imported, TensorFlow fails to initialize its native
runtime. Importing this module first preloads the up-to-date system runtime
DLLs, so both libraries share the current versions.

Import this module before PyQt5 and tensorflow in every entry point or
module that uses both.
"""
import sys

if sys.platform == "win32":
    import ctypes

    for _dll in ("vcruntime140.dll", "vcruntime140_1.dll", "msvcp140.dll",
                 "msvcp140_1.dll", "msvcp140_2.dll", "concrt140.dll"):
        try:
            ctypes.WinDLL(_dll)
        except OSError:
            pass
