import pytest
import numpy as np
from loadimg import load_img

from selective_editor.app import upload, reset_fn


@pytest.fixture
def mock_base_img():
    return np.zeros((100, 100, 3), dtype=np.uint8)


def test_upload():
    test_img = np.zeros((100, 100, 3), dtype=np.uint8)
    result_img, result_mask, result_legend = upload(test_img)

    assert result_img is test_img
    assert result_mask is None
    assert result_legend is None


def test_upload_none():
    result_img, result_mask, result_legend = upload()
    assert result_img is None
    assert result_mask is None
    assert result_legend is None


def test_reset_fn(mock_base_img):
    result_base, result_img, result_legend, result_mask = reset_fn(
        mock_base_img,
        mock_base_img,
        {"points": [1], "labels": [1]},
        load_img(np.zeros((100, 100))),
    )

    assert result_base is mock_base_img
    assert result_img is mock_base_img
    assert result_legend is None
    assert result_mask is None


def test_reset_fn_with_none_inputs():
    result_base, result_img, result_legend, result_mask = reset_fn(
        None, None, None, None
    )
    assert result_base is None
    assert result_img is None
    assert result_legend is None
    assert result_mask is None
