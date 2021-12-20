import pickle

import numpy as np
from flask import jsonify

from api.preparation import extract_filenames
from api.preprocess import get_shrinked_img


def evaluate_probs(request) -> tuple:
    """テストデータを利用してロジスティック回帰の学習済みモデルのアウトプットを評価"""
    file_id = request.json["file_id"]
    filenames = extract_filenames(file_id)
    img_test = get_shrinked_img(filenames)

    with open("model.pickle", mode="rb") as fp:
        model = pickle.load(fp)

    X_true = [int(filename[:1]) for filename in filenames]
    X_true = np.array(X_true)

    predicted_result = model.predict(img_test).tolist()
    accuracy = model.score(img_test, X_true).tolist()
    observed_result = X_true.tolist()

    return jsonify(
        {
            "results": {
                "file_id": file_id,
                "observed_result": observed_result,
                "predicted_result": predicted_result,
                "accuracy": accuracy,
            }
        },
        201,
    )
