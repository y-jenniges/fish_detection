"""
Tests for stereo rectification, left/right matching and length
calculation against the calibration in src/config.json and the example
stereo image pair.
"""
import numpy as np
import pytest

from maromarker.processing import post_processing as pp
from maromarker.processing.distance_measurer import DistanceMeasurer
from conftest import IMAGE_SIZE


@pytest.fixture(scope="module")
def matcher(camera_config):
    return pp.StereoCorrespondence(
        camera_config["mtx_L"], camera_config["dist_L"],
        camera_config["mtx_R"], camera_config["dist_R"],
        camera_config["R"], camera_config["T"], IMAGE_SIZE)


@pytest.fixture(scope="module")
def measurer(camera_config):
    return DistanceMeasurer(
        camera_config["mtx_L"], camera_config["dist_L"],
        camera_config["mtx_R"], camera_config["dist_R"],
        camera_config["R"], camera_config["T"], IMAGE_SIZE)


class TestStereoCorrespondence:
    def test_undistort_distort_roundtrip(self, matcher):
        point = [2000.0, 1400.0]
        rectified = matcher.undistortPoint(point, "L")
        restored = matcher.distortPoint(rectified, "L")
        assert restored[0] == pytest.approx(point[0], abs=2.0)
        assert restored[1] == pytest.approx(point[1], abs=2.0)

    def test_same_vec(self, matcher):
        assert matcher.sameVec([100, 0], [101, 1])
        assert not matcher.sameVec([100, 0], [-100, 0])

    def test_rectify_and_match_structure(self, matcher, camera_config,
                                         example_paths):
        # two synthetic animals on the left image (group, y1, x1, y2,
        # x2, row index)
        animals_left = [[0, 1400.0, 2000.0, 1500.0, 2200.0, 0],
                        [0, 700.0, 1000.0, 800.0, 1200.0, 1]]
        merged = matcher.rectifyAndMatch(
            camera_config, example_paths["img_l"], example_paths["img_r"],
            animals_left)

        assert len(merged) == len(animals_left)
        for obj in merged:
            # group, 4 left coords, 4 right coords
            assert len(obj) == 9

    def test_rectify_and_match_no_animals(self, matcher, camera_config,
                                          example_paths):
        merged = matcher.rectifyAndMatch(
            camera_config, example_paths["img_l"], example_paths["img_r"],
            [])
        assert merged == ([], []) or merged == []


class TestDistanceMeasurer:
    def test_nan_for_unmatched_animal(self, measurer):
        d = measurer.distances(np.array([[100.0, 100.0]]),
                               np.array([[200.0, 200.0]]),
                               np.array([[0.0, 0.0]]),
                               np.array([[0.0, 0.0]]))
        assert d == ["NaN"]

    def test_positive_distance_for_matched_animal(self, measurer):
        # a plausible correspondence with some disparity
        d = measurer.distances(np.array([[2000.0, 1400.0]]),
                               np.array([[2200.0, 1500.0]]),
                               np.array([[1900.0, 1400.0]]),
                               np.array([[2100.0, 1500.0]]))
        assert len(d) == 1
        assert isinstance(d[0], float)
        assert d[0] > 0

    def test_distance_is_stable(self, measurer):
        args = (np.array([[2000.0, 1400.0]]), np.array([[2200.0, 1500.0]]),
                np.array([[1900.0, 1400.0]]), np.array([[2100.0, 1500.0]]))
        assert measurer.distances(*args) == measurer.distances(*args)
