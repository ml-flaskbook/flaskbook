import numpy as np
from api.preprocess import get_grayscale, get_shrinked_img, shrink_image
from PIL import Image


def test_get_grayscale(app):
    # SET
    test_data = [
        "0.jpg",
        "1.jpg",
        "2.jpg",
        "3.jpg",
        "4.jpg",
        "5.jpg",
        "6.jpg",
        "7.jpg",
        "8.jpg",
        "9.jpg",
    ]

    def mock_generator():
        yield from ()

    expected_generator = mock_generator()
    expected_len = 10

    # EXECUTE
    actual_data = get_grayscale(test_data)
    # CHECK
    assert type(expected_generator) == type(actual_data)
    assert expected_len == len(list(actual_data))


def test_shrink_image(app):
    # SET
    mock_objs = [Image.new("L", (64, 64)) for _ in range(10)]
    expected_data = np.array([np.nan for _ in range(64)])
    expected_len = 8
    # EXECUTE
    for mock_obj in mock_objs:
        actual_data = shrink_image(mock_obj)
        # CHECK
        assert expected_len == len(actual_data)
        assert isinstance(actual_data, (np.ndarray, np.generic))
        assert expected_data.all() == actual_data.all()


def test_get_shrinked_img(app):
    # SET
    test_data = [
        "0.jpg",
        "1.jpg",
        "2.jpg",
        "3.jpg",
        "4.jpg",
        "5.jpg",
        "6.jpg",
        "7.jpg",
        "8.jpg",
        "9.jpg",
    ]
    expected_len = 10

    # EXECUTE
    actual_data = get_shrinked_img(test_data)

    # CHECK
    assert expected_len == len(actual_data)
    assert isinstance(actual_data, (np.ndarray, np.generic))
