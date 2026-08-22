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


def match_stereo_pairs(l_paths, r_paths):
    """ Matches left and right images by file ID, i.e. ignoring
    STEREO_SUFFIXES and IMAGE_EXTENSIONS. Images without a
    matching counterpart are dropped, and returned separately so the
    caller can warn about them.

    Returns
    -------
    (list<str>, list<str>, list<str>, list<str>)
        The matched left paths, the matched right paths, the left
        paths that had no matching right image, and the right paths
        that had no matching left image.
    """
    # index right images by file ID
    r_by_id = {}
    for r_path in r_paths:
        r_by_id[file_id_from_path(r_path)] = r_path

    # sort left images
    l_paths_sorted = list(l_paths)
    l_paths_sorted.sort()

    # iterate left images in order and look up the matching right image
    matched_l = []
    matched_r = []
    unmatched_l = []
    matched_ids = set()
    for l_path in l_paths_sorted:
        # get left image id
        file_id = file_id_from_path(l_path)

        # match to right image id
        if file_id in r_by_id:
            matched_l.append(l_path)
            matched_r.append(r_by_id[file_id])
            matched_ids.add(file_id)
        else:
            # no right image found for this left image
            unmatched_l.append(l_path)

    # right images whose id was never matched to a left image
    unmatched_r = [r_path for file_id, r_path in r_by_id.items()
                   if file_id not in matched_ids]
    unmatched_r.sort()

    return matched_l, matched_r, unmatched_l, unmatched_r
