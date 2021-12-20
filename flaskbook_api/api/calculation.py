from os import abort
from pathlib import Path

import numpy as np
import cv2
import torch
from flask import current_app, jsonify

from flaskbook_api.api.postprocess import draw_lines, draw_texts, make_color, make_line
from flaskbook_api.api.preparation import load_image
from flaskbook_api.api.preprocess import image_to_tensor

basedir = Path(__file__).parent.parent


def detection(request):
    dict_results = {}
    # ラベルの読み込み
    labels = current_app.config["LABELS"]
    # 画像の読み込み
    image, filename = load_image(request)
    # 画像データをテンソル型の数値データへ変更
    image_tensor = image_to_tensor(image)

    # 学習済みモデルの読み込み
    try:
        model = torch.load("model.pt")
    except FileNotFoundError:
        return jsonify("The model is not found"), 404

    # モデルの推論モードに切り替え
    model = model.eval()
    # 推論の実行
    output = model([image_tensor])[0]

    result_image = np.array(image.copy())
    # 学習済みモデルが検知した物体の画像に枠線とラベルを追記
    for box, label, score in zip(output["boxes"], output["labels"], output["scores"]):
        # スコアが0.6以上と重複していないラベルに絞り込み
        if score > 0.6 and labels[label] not in dict_results:
            # 枠線の色の決定
            color = make_color(labels)
            # 枠線の作成
            line = make_line(result_image)
            # 検知画像の枠線とテキストラベルの枠線の位置情報
            c1 = (int(box[0]), int(box[1]))
            c2 = (int(box[2]), int(box[3]))
            # 画像に枠線を追記
            draw_lines(c1, c2, result_image, line, color)
            # 画像にテキストラベルを追記
            draw_texts(result_image, line, c1, color, labels[label])
            # 検知されたラベルとスコアの辞書を作成
            dict_results[labels[label]] = round(100 * score.item())
    # 画像保存先のディレクトリのフルパスを作成
    dir_image = str(basedir / "data" / "output" /filename)

    # 検知後の画像ファイルを保存
    cv2.imwrite(dir_image, cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))
    return jsonify(dict_results), 201
