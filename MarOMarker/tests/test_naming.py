"""
Tests for file ID derivation from stereo image file names.

These lock in the fix for the old rstrip based logic, which stripped
trailing characters (any of ".jpgpn_LR") instead of a suffix and so
corrupted file IDs ending in one of those characters.
"""
from maromarker.naming import file_id_from_path


class TestFileIdFromPath:
    def test_left_and_right_share_id(self):
        left = file_id_from_path("TN_Exif_Remos1_2016.04.28_01.30.54_L.jpg")
        right = file_id_from_path("TN_Exif_Remos1_2016.04.28_01.30.54_R.jpg")
        assert left == right == "TN_Exif_Remos1_2016.04.28_01.30.54"

    def test_full_path_uses_basename(self):
        p = "T:/data/2017_09/some_image_L.jpg"
        assert file_id_from_path(p) == "some_image"

    def test_png_extension(self):
        assert file_id_from_path("frame_042_R.png") == "frame_042"

    def test_id_ending_in_stripped_char_is_preserved(self):
        # the old rstrip logic would corrupt these: 'g' and 'p' are in
        # ".jpg", and a trailing 'L'/'R' after the suffix removal
        assert file_id_from_path("catalog_L.jpg") == "catalog"
        assert file_id_from_path("group_R.jpg") == "group"
        assert file_id_from_path("STEREO_R_L.jpg") == "STEREO_R"

    def test_no_stereo_suffix(self):
        assert file_id_from_path("plain_image.jpg") == "plain_image"

    def test_case_insensitive_extension(self):
        assert file_id_from_path("IMG_5_L.JPG") == "IMG_5"
