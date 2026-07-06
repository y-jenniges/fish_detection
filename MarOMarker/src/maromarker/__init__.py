"""
MarOMarker (Marine Organism Marker) - semi-automatic annotation and
measurement of marine organisms on stereoscopic underwater photographs.
"""

# Preload the system MSVC runtime DLLs before any submodule imports
# PyQt5 or TensorFlow. The PyQt5 Qt wheel bundles outdated copies that
# break TensorFlow initialization if Qt loads them first. Doing this at
# package import time makes it deterministic regardless of the order in
# which submodules are imported (app, pytest, Sphinx autodoc, ...).
from maromarker import win_dll_compat as _win_dll_compat  # noqa: F401

__version__ = "2.0.0.dev0"
