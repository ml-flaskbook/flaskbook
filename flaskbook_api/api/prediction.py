from flask import current_app, jsonify, json
from flaskbook_api.api.preprocess import preprocess_example

def prediction_example(request):
    results_dict = {}
    request_data = json.loads(request.data)
    filename = request_data["filename"]

    # 前処理
    image_preprocessed = preprocess_example(filename)

    # 推論

    # 後処理
    results_dict["result"] = "OK"
    results_dict["input"] = request_data

    return jsonify(results_dict), 201