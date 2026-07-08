"""
Helpers for deriving file IDs from stereo image file names.

The stereo pairs are named <file_id>_L.<ext> and <file_id>_R.<ext>.
The file ID is the base name without the image extension and without
the left/right suffix.
"""
import os

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")
STEREO_SUFFIXES = ("_L", "_R")


def file_id_from_path(path):
    """
    Returns the file ID for a stereo image path, i.e. the base name
    without its image extension and without the _L/_R stereo suffix.

    Parameters
    ----------
    path : string
        Path to a stereo image file.

    Returns
    -------
    string
        The file ID shared by the left and right image of a pair.
    """
    name = os.path.basename(path)
    root, ext = os.path.splitext(name)
    if ext.lower() in IMAGE_EXTENSIONS:
        name = root
    for suffix in STEREO_SUFFIXES:
        if name.endswith(suffix):
            return name[:-len(suffix)]
    return name
