import json

from flask import Blueprint, jsonify, request

from api import calculation, preparation

from .json_validate import validate_json, validate_schema

api = Blueprint("api", __name__, url_prefix="/v1")


@api.post("/file-id")
@validate_json
@validate_schema("check_dir_name")
def file_id():
    return preparation.insert_filenames(request)


@api.post("/probabilities")
@validate_json
@validate_schema("check_file_id")
def probabilities():
    return calculation.evaluate_probs(request)


@api.post("/check-schema")
# json schemaの有無のチェックをするデコレーター
@validate_json
# json schemaの定義があっているかどうかのチェックをするデコレーター
@validate_schema("check_file_schema")
def check_schema():
    data = json.loads(request.data)
    print(data["file_id"])
    print(data["file_name"])
    d = data["file_name"]
    return f"Successfully get {d}"


@api.errorhandler(400)
@api.errorhandler(404)
@api.errorhandler(500)
def error_handler(error):
    response = jsonify(
        {"error_message": error.description["error_message"], "result": error.code}
    )
    return response, error.code
