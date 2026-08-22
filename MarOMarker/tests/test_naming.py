"""
Tests for file ID derivation from stereo image file names.

These lock in the fix for the old rstrip based logic, which stripped
trailing characters (any of ".jpgpn_LR") instead of a suffix and so
corrupted file IDs ending in one of those characters.
"""
from maromarker.naming import file_id_from_path, match_stereo_pairs


class TestFileIdFromPath:
    def test_left_and_right_share_id(self):
        # get id for both images
        left = file_id_from_path("TN_Exif_Remos1_2016.04.28_01.30.54_L.jpg")
        right = file_id_from_path("TN_Exif_Remos1_2016.04.28_01.30.54_R.jpg")

        # ids should match
        assert left == right == "TN_Exif_Remos1_2016.04.28_01.30.54"

    def test_full_path_uses_basename(self):
        # use full path with directory
        p = "T:/data/2017_09/some_image_L.jpg"
        assert file_id_from_path(p) == "some_image"

    def test_png_extension(self):
        # use png instead of jpg
        assert file_id_from_path("frame_042_R.png") == "frame_042"

    def test_id_ending_in_stripped_char_is_preserved(self):
        # the old rstrip logic would corrupt these: 'g' and 'p' are in
        # ".jpg", and a trailing 'L'/'R' after the suffix removal
        assert file_id_from_path("catalog_L.jpg") == "catalog"
        assert file_id_from_path("group_R.jpg") == "group"
        assert file_id_from_path("STEREO_R_L.jpg") == "STEREO_R"

    def test_no_stereo_suffix(self):
        # no L/R suffix
        assert file_id_from_path("plain_image.jpg") == "plain_image"

    def test_case_insensitive_extension(self):
        # use uppercase extension
        assert file_id_from_path("IMG_5_L.JPG") == "IMG_5"


class TestMatchStereoPairs:
    def test_matches_by_id_regardless_of_input_order(self):
        # test shuffled lists
        l_paths = [
            "cam_2020.01.01_12.00.02_L.jpg",
            "cam_2020.01.01_12.00.01_L.jpg",
            "cam_2020.01.01_12.00.03_L.jpg",
        ]
        r_paths = [
            "cam_2020.01.01_12.00.03_R.jpg",
            "cam_2020.01.01_12.00.01_R.jpg",
            "cam_2020.01.01_12.00.02_R.jpg",
        ]
        matched_l, matched_r, unmatched_l, unmatched_r = match_stereo_pairs(l_paths, r_paths)

        # left images should come back sorted, matched to the right id
        assert matched_l == [
            "cam_2020.01.01_12.00.01_L.jpg",
            "cam_2020.01.01_12.00.02_L.jpg",
            "cam_2020.01.01_12.00.03_L.jpg",
        ]

        # check the pairs match
        for l_path, r_path in zip(matched_l, matched_r):
            assert file_id_from_path(l_path) == file_id_from_path(r_path)

        # no unmatched images in this case
        assert unmatched_l == []
        assert unmatched_r == []

    def test_left_image_without_right_counterpart_is_dropped(self):
        # b has no right image
        matched_l, matched_r, unmatched_l, unmatched_r = match_stereo_pairs(
            ["a_L.jpg", "b_L.jpg"], ["a_R.jpg"])

        # only a should remain, b should be reported as unmatched
        assert matched_l == ["a_L.jpg"]
        assert matched_r == ["a_R.jpg"]
        assert unmatched_l == ["b_L.jpg"]
        assert unmatched_r == []

    def test_right_image_without_left_counterpart_is_dropped(self):
        # b has no left image
        matched_l, matched_r, unmatched_l, unmatched_r = match_stereo_pairs(
            ["a_L.jpg"], ["a_R.jpg", "b_R.jpg"])

        # only a should remain, b should be reported as unmatched
        assert matched_l == ["a_L.jpg"]
        assert matched_r == ["a_R.jpg"]
        assert unmatched_l == []
        assert unmatched_r == ["b_R.jpg"]

    def test_no_matches_returns_empty_lists(self):
        # ids do not overlap
        matched_l, matched_r, unmatched_l, unmatched_r = match_stereo_pairs(["a_L.jpg"], ["b_R.jpg"])
        assert matched_l == []
        assert matched_r == []

        # a is left over with no right counterpart, and vice versa for b
        assert unmatched_l == ["a_L.jpg"]
        assert unmatched_r == ["b_R.jpg"]
