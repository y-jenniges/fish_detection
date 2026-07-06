"""
Tests for the table model backing the result CSV files. The CSV column
layout is frozen here on purpose: existing result files and downstream
analyses depend on it, so any change to getColumns or exportToCsv that
alters the format must fail these tests.
"""
import os

import pandas as pd
import pytest

# the exact historical column layout of results_yyyy_MM.csv files
EXPECTED_COLUMNS = [
    "file_id", "object_remarks", "group", "species",
    "LX1", "LY1", "LX2", "LY2", "LX3", "LY3", "LX4", "LY4",
    "RX1", "RY1", "RX2", "RY2", "RX3", "RY3", "RX4", "RY4",
    "length", "height", "image_remarks", "status",
    "manually_corrected", "experiment_id", "user_id",
]


@pytest.fixture()
def models(qapp):
    from maromarker.core.models import Models
    m = Models()
    m.model_animals.update(
        pd.DataFrame(columns=m.model_animals.getColumns()))
    return m


def _make_row(models, file_id="TN_Exif_Remos1_2016.04.28_01.30.54",
              group="Fish"):
    row = {c: -1 for c in models.model_animals.getColumns()}
    row.update({"file_id": file_id, "object_remarks": "", "group": group,
                "species": "Unidentified", "image_remarks": "",
                "status": "not checked", "manually_corrected": "False",
                "experiment_id": "exp", "user_id": "yj"})
    return row


class TestCsvFormat:
    def test_column_layout_is_frozen(self, models):
        assert list(models.model_animals.getColumns()) == EXPECTED_COLUMNS

    def test_export_new_file_has_expected_header(self, models, tmp_path):
        models.model_animals.exportToCsv(str(tmp_path), "results_2016_04.csv")
        out = pd.read_csv(tmp_path / "results_2016_04.csv")
        assert list(out.columns) == EXPECTED_COLUMNS

    def test_export_roundtrip_preserves_data(self, models, tmp_path):
        df = pd.DataFrame([_make_row(models)])
        models.model_animals.insertDfRows(0, 1, df)
        models.model_animals.exportToCsv(str(tmp_path), "results_2016_04.csv")

        out = pd.read_csv(tmp_path / "results_2016_04.csv")
        assert len(out) == 1
        assert out.loc[0, "group"] == "Fish"
        assert out.loc[0, "file_id"] == "TN_Exif_Remos1_2016.04.28_01.30.54"
        assert list(out.columns) == EXPECTED_COLUMNS

    def test_snapshot_writes_all_rows(self, models, tmp_path):
        # the autosave safety net calls exportToCsv without a file_id,
        # which must write the complete in-memory table as a snapshot
        df = pd.DataFrame([_make_row(models, file_id="img_a"),
                           _make_row(models, file_id="img_b", group="Jellyfish"),
                           _make_row(models, file_id="img_c")])
        models.model_animals.insertDfRows(0, 3, df)

        # a pre-existing snapshot file must be fully overwritten, not merged
        (tmp_path / "results_2016_04_inProgress.csv").write_text("stale")
        models.model_animals.exportToCsv(
            str(tmp_path), "results_2016_04_inProgress.csv")

        out = pd.read_csv(tmp_path / "results_2016_04_inProgress.csv")
        assert len(out) == 3
        assert set(out["file_id"]) == {"img_a", "img_b", "img_c"}


class TestTableModel:
    def test_insert_df_rows(self, models):
        df = pd.DataFrame([_make_row(models), _make_row(models, group="Crustacea")])
        models.model_animals.insertDfRows(0, 2, df)
        assert len(models.model_animals.data) == 2

    def test_remove_rows(self, models):
        df = pd.DataFrame([_make_row(models), _make_row(models)])
        models.model_animals.insertDfRows(0, 2, df)
        models.model_animals.removeRows(0, 1)
        assert len(models.model_animals.data) == 1

    def test_load_file_normalizes_nan_remarks(self, models, tmp_path):
        row = _make_row(models)
        df = pd.DataFrame([row])
        df.loc[0, "object_remarks"] = float("nan")
        df.loc[0, "image_remarks"] = float("nan")
        path = tmp_path / "results_2016_04.csv"
        df.to_csv(path, index=False)

        models.model_animals.loadFile(str(path))
        assert models.model_animals.data.loc[0, "object_remarks"] == ""
        assert models.model_animals.data.loc[0, "image_remarks"] == ""

    def test_load_file_rejects_wrong_columns(self, models, tmp_path):
        before = len(models.model_animals.data)
        path = tmp_path / "bad.csv"
        pd.DataFrame({"foo": [1]}).to_csv(path, index=False)
        models.model_animals.loadFile(str(path))
        assert len(models.model_animals.data) == before


class TestAnimal:
    def test_remark_nan_normalized(self, models):
        from PyQt5 import QtCore
        from maromarker.ui.animal import Animal
        a = Animal(models, 0, QtCore.QPointF(10, 10),
                   QtCore.QPointF(50, 50), "Fish", "Unidentified",
                   remark=float("nan"))
        assert a.remark == ""

    def test_creation_and_marker_moves(self, models):
        from PyQt5 import QtCore
        from maromarker.ui.animal import Animal
        a = Animal(models, 0, QtCore.QPointF(100, 150),
                   QtCore.QPointF(300, 350), "Fish", "Unidentified")
        a.createHeadVisual()
        a.createTailVisual()
        a.setPositionHead(QtCore.QPoint(120, 160))
        a.setPositionTail(QtCore.QPoint(280, 340))
        a.calculateBoundingBox()
        assert a.boundingBox.width() > 0
        assert a.boundingBox.height() > 0
