"""
Shared pytest fixtures for the MarOMarker test suite.

The maromarker package lives under src/, so src is put on sys.path
here. A single QApplication is created for the whole session, since the
Qt-based models and widgets require one.
"""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
sys.path.insert(0, SRC)

EXAMPLE_DIR = os.path.join(ROOT, "example_usage")
IMG_L = os.path.join(EXAMPLE_DIR, "input_images", "2016_04",
                     "TN_Exif_Remos1_2016.04.28_01.30.54_L.jpg")
IMG_R = os.path.join(EXAMPLE_DIR, "input_images", "2016_04",
                     "TN_Exif_Remos1_2016.04.28_01.30.54_R.jpg")
MODEL_PATH = os.path.join(EXAMPLE_DIR, "neural_network_model")
CONFIG_PATH = os.path.join(SRC, "maromarker", "config.json")

# original image resolution of the example stereo camera setup
IMAGE_SIZE = (4272, 2848)


@pytest.fixture(scope="session")
def qapp():
    """ Session-wide QApplication required by Qt models and widgets. """
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    return app


@pytest.fixture(scope="session")
def camera_config():
    """ The stereo camera calibration shipped in src/config.json. """
    import json
    with open(CONFIG_PATH) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def example_paths():
    """ Paths to the example stereo pair and neural network model. """
    return {"img_l": IMG_L, "img_r": IMG_R, "model": MODEL_PATH}
