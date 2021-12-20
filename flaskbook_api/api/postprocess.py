import random

import cv2


def make_color(labels):
    """枠線の色をランダムに決定"""
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in labels]
    color = random.choice(colors)
    return color


def make_line(result_image):
    """枠線を作成"""
    line = round(0.002 * max(result_image.shape[0:2])) + 1
    return line


def draw_lines(c1, c2, result_image, line, color):
    """枠線を追記"""
    cv2.rectangle(result_image, c1, c2, color, thickness=line)


def draw_texts(result_image, line, c1, color, display_txt):
    """検知したテキストラベルを画像に追記"""
    # テキストサイズの取得
    font = max(line - 1, 1)
    t_size = cv2.getTextSize(display_txt, 0, fontScale=line / 3, thickness=font)[0]
    c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3

    # テキストボックスの追加
    cv2.rectangle(result_image, c1, c2, color, -1)
    # テキストラベル及びテキストボックスの加工
    cv2.putText(
        result_image,
        display_txt,
        (c1[0], c1[1] - 2),
        0,
        line / 3,
        [225, 255, 255],
        thickness=font,
        lineType=cv2.LINE_AA,
    )