"""
Tests for neural network loading and prediction. These load TensorFlow
and run a real inference, so they are the slowest part of the suite
(marked as slow).
"""
import pytest

pytestmark = pytest.mark.slow


@pytest.fixture(scope="module")
def predicter(qapp, example_paths):
    from maromarker.processing import predicter as Predicter
    p = Predicter.Predicter()
    assert p.loadNeuralNet(example_paths["model"])
    return p


class TestModelLoading:
    def test_extensionless_h5_loads(self, predicter):
        assert predicter.neural_network is not None

    def test_expected_input_shape(self, predicter):
        # the example model works on 25 percent downscaled images padded
        # to a multiple of 32
        assert predicter.neural_network.input_shape == (None, 736, 1088, 3)


class TestPrediction:
    def test_predict_image_returns_animals(self, predicter, example_paths):
        df = predicter.predictImage(example_paths["img_l"], "file_id_test",
                                    "exp", "usr")
        # the example image contains animals; the reference run found 10
        assert len(df) > 0
        for col in ["file_id", "group", "species", "LX1", "LY1", "LX2",
                    "LY2"]:
            assert col in df.columns
        assert (df["file_id"] == "file_id_test").all()
        # coordinates must lie inside the original image resolution
        assert df["LX1"].between(0, 4272).all()
        assert df["LY1"].between(0, 2848).all()
