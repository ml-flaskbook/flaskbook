from flask import Blueprint, jsonify, request
from flaskbook_api.api import prediction

api = Blueprint("api", __name__)

@api.get("/")
def index():
    return jsonify({"column": "value"}), 201

@api.post("/prediction_example")
def detection():
    return prediction.prediction_example(request)
