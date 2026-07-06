"""
Tests for the GUI-free helper functions in PostProcessing: head/tail
matching, heatmap coordinate extraction, coordinate scaling and image
loading for the neural network.
"""
import numpy as np
import pytest

import PostProcessing as pp
from conftest import IMG_L


class TestWeightedEuclidean:
    def test_zero_distance(self):
        assert pp.weightedEuclidean(0, 0) == 0

    def test_known_value(self):
        # weights: a=0.54 in x, b=0.46 in y
        expected = np.sqrt(0.54 * 9 + 0.46 * 16)
        assert pp.weightedEuclidean(3, 4) == pytest.approx(expected)

    def test_x_weighted_more_than_y(self):
        assert pp.weightedEuclidean(10, 0) > pp.weightedEuclidean(0, 10)


class TestFindHeadTailMatches:
    def test_no_tails_gives_no_matches(self):
        matches = pp.findHeadTailMatches([(10, 10)], [])
        assert len(matches) == 0

    def test_no_heads_gives_no_matches(self):
        matches = pp.findHeadTailMatches([], [(10, 10)])
        assert len(matches) == 0

    def test_single_pair(self):
        matches = pp.findHeadTailMatches([(0, 0)], [(5, 5)])
        assert matches.shape == (1, 2, 2)
        assert (matches[0][0] == (0, 0)).all()
        assert (matches[0][1] == (5, 5)).all()

    def test_two_pairs_matched_by_distance(self):
        # heads and tails are given in (y, x); each head should pair
        # with its nearby tail, not with the far one
        heads = [(0, 0), (100, 100)]
        tails = [(102, 98), (3, 2)]
        matches = pp.findHeadTailMatches(heads, tails)
        assert matches.shape == (2, 2, 2)
        pairs = {tuple(m[0]): tuple(m[1]) for m in matches}
        assert pairs[(0, 0)] == (3, 2)
        assert pairs[(100, 100)] == (102, 98)

    def test_more_heads_than_tails(self):
        heads = [(0, 0), (50, 50), (100, 100)]
        tails = [(1, 1)]
        matches = pp.findHeadTailMatches(heads, tails)
        assert matches.shape == (1, 2, 2)
        assert (matches[0][0] == (0, 0)).all()


class TestScaleMatchCoordinates:
    def test_identity_scaling(self):
        matches = np.array([[(10, 20), (30, 40)]])
        scaled = pp.scaleMatchCoordinates(matches, (100, 100), (100, 100))
        assert (scaled == matches).all()

    def test_upscaling(self):
        matches = np.array([[(10, 20), (30, 40)]])
        scaled = pp.scaleMatchCoordinates(matches, (100, 200), (200, 100))
        # x scaled by 2, y scaled by 0.5
        assert (scaled[0][0] == (20, 10)).all()
        assert (scaled[0][1] == (60, 20)).all()

    def test_empty(self):
        scaled = pp.scaleMatchCoordinates([], (100, 100), (200, 200))
        assert len(scaled) == 0


class TestFindCoordinates:
    def test_two_separated_blobs(self):
        hm = np.zeros((100, 100), dtype="uint8")
        hm[20, 30] = 255
        hm[70, 80] = 255
        coords = pp.findCoordinates(hm, threshold=50, radius=5)
        # output is in (x, y) order
        found = {tuple(c) for c in coords}
        assert found == {(30, 20), (80, 70)}

    def test_close_points_are_merged(self):
        hm = np.zeros((100, 100), dtype="uint8")
        hm[50, 50] = 255
        hm[54, 54] = 255
        coords = pp.findCoordinates(hm, threshold=50, radius=1)
        assert len(coords) == 1

    def test_below_threshold_ignored(self):
        hm = np.zeros((100, 100), dtype="uint8")
        hm[20, 30] = 40
        coords = pp.findCoordinates(hm, threshold=50, radius=5)
        assert len(coords) == 0


class TestApplyThresholdToHm:
    def test_threshold(self):
        img = np.array([[10, 60, 200]], dtype="uint8")
        out = pp.applyThresholdToHm(img, threshold=50)
        assert out[0, 0] == 0
        assert out[0, 1] == 60
        assert out[0, 2] == 200


class TestLoadImage:
    def test_shape_padded_to_factor_and_range(self):
        img = pp.loadImage(IMG_L, factor=32)
        assert img.shape[0] % 32 == 0
        assert img.shape[1] % 32 == 0
        assert img.shape[2] == 3
        assert img.min() >= -1.0
        assert img.max() <= 1.0

    def test_large_image_is_downscaled(self):
        # the example images are 2848x4272, so they must be resized to
        # 25 percent and then padded to a multiple of 32
        img = pp.loadImage(IMG_L, factor=32)
        assert img.shape[0] == 736
        assert img.shape[1] == 1088
