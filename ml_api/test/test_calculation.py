import pytest
from api.calculation import evaluate_probs
from api.models import ImageInfo, db


@pytest.fixture
def app_made_preparation(app):
    file_id = "test_file_id"
    filenames = [
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

    with app.app_context():
        for filename in filenames:
            image_info = ImageInfo(file_id=file_id, filename=filename)
            db.session.add(image_info)
        db.session.commit()
    return app


def test_evaluate_probs(app_made_preparation):
    # SET
    path = "/v1/evaluate_probs"
    payload = {"file_id": "test_file_id"}

    expected_file_id = "test_file_id"
    expected_data_len = 10

    # EXECUTE
    with app_made_preparation.test_request_context(
        path, method="POST", json=payload
    ) as req:
        json_response = evaluate_probs(req.request)

    actual_file_id = json_response.json[0]["results"]["file_id"]
    actual_observed_result = json_response.json[0]["results"]["observed_result"]
    actual_predicted_result = json_response.json[0]["results"]["predicted_result"]
    actual_accuracy = json_response.json[0]["results"]["accuracy"]

    # CHECK
    assert expected_file_id == actual_file_id
    assert expected_data_len == len(actual_observed_result)
    assert expected_data_len == len(actual_predicted_result)
    assert isinstance(actual_accuracy, float)