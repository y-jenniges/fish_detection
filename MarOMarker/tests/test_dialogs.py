"""
Tests for the mismatch dialog result codes. The non-modal match flow
(image_areas.ImageAreaLR) relies on these exact codes: 0 = keep left,
1 = keep right, 2 = merge, -1 = cancel/abort.
"""
from maromarker.ui.helpers import MismatchDialog


def test_button_a_returns_0(qapp):
    dlg = MismatchDialog("t", "text", "A", "B", "C")
    dlg.on_btn_a()
    assert dlg.result() == 0


def test_button_b_returns_1(qapp):
    dlg = MismatchDialog("t", "text", "A", "B", "C")
    dlg.on_btn_b()
    assert dlg.result() == 1


def test_button_c_returns_2(qapp):
    dlg = MismatchDialog("t", "text", "A", "B", "C")
    dlg.on_btn_c()
    assert dlg.result() == 2


def test_cancel_returns_minus_1(qapp):
    dlg = MismatchDialog("t", "text", "A", "B", "C")
    dlg.on_cancel()
    assert dlg.result() == -1


def test_reject_counts_as_cancel(qapp):
    # closing via the window frame or Escape must abort, not silently
    # pick an option
    dlg = MismatchDialog("t", "text", "A", "B")
    dlg.reject()
    assert dlg.result() == -1


def test_finished_signal_carries_result(qapp):
    dlg = MismatchDialog("t", "text", "A", "B", "C")
    received = []
    dlg.finished.connect(received.append)
    dlg.on_btn_b()
    assert received == [1]
