import uuid

import pytest
from api.models import ImageInfo, db
from api.preparation import extract_filenames, insert_filenames, load_filenames


@pytest.fixture
def app_made_preparation(app):
    file_id = "test_file_id"
    filenames = [
        "test0.jpg",
        "test1.jpg",
        "test2.jpg",
        "test3.jpg",
        "test4.jpg",
        "test5.jpg",
        "test6.jpg",
        "test7.jpg",
        "test8.jpg",
        "test9.jpg",
    ]

    with app.app_context():
        for filename in filenames:
            image_info = ImageInfo(file_id=file_id, filename=filename)
            db.session.add(image_info)
        db.session.commit()
    return app


def test_load_filenames(app):
    # SET
    test_data = "handwriting_pics"
    expected_data = [
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

    # EXECUTE
    actual_data = load_filenames(test_data)

    # CHECK
    assert len(expected_data) == len(actual_data)
    assert sorted(expected_data) == sorted(actual_data)


def test_insert_filenames(app):
    # SET
    path = "/v1/insert_filenames"
    payload = {"dir_name": "handwriting_pics"}

    # EXECUTE
    with app.test_request_context(path, method="POST", json=payload) as req:
        json_response = insert_filenames(req.request)

    actual_data = json_response[0].json["file_id"]

    # CHECK
    assert isinstance(actual_data, str)
    assert uuid.UUID(actual_data).version == 4


def test_extract_filenames(app_made_preparation):
    # SET
    test_data = "test_file_id"
    expected_data = [
        "test0.jpg",
        "test1.jpg",
        "test2.jpg",
        "test3.jpg",
        "test4.jpg",
        "test5.jpg",
        "test6.jpg",
        "test7.jpg",
        "test8.jpg",
        "test9.jpg",
    ]

    # EXECUTE
    actual_data = extract_filenames(test_data)

    # CHECK
    assert len(expected_data) == len(actual_data)
    assert sorted(expected_data) == sorted(actual_data)
    assert all([a == b for a, b in zip(expected_data, actual_data)])
