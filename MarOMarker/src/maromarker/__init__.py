"""
MarOMarker (Marine Organism Marker) - semi-automatic annotation and
measurement of marine organisms on stereoscopic underwater photographs.
"""

# preload the system MSVC runtime DLLs before any submodule imports PyQt5 or
# TensorFlow (see win_dll_compat); doing it here makes it order-independent
from maromarker import win_dll_compat as _win_dll_compat  # noqa: F401

__version__ = "2.0.0.dev0"
