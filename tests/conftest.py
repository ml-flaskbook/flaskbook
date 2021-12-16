import os
import shutil

import pytest
from apps.app import create_app, db
from apps.crud.models import User
from apps.detector.models import UserImage, UserImageTag


# フィクスチャ関数を作成する
@pytest.fixture
def fixture_app():
    # セットアップ処理
    # テスト用のコンフィグを使うために引数にtestingを指定する
    app = create_app("testing")

    # データベースを利用するための宣言をする
    app.app_context().push()

    # テスト用データベースのテーブルを作成する
    with app.app_context():
        db.create_all()

    # テスト用の画像アップロードディレクトリを作成する
    os.mkdir(app.config["UPLOAD_FOLDER"])

    # テストを実行する
    yield app

    # クリーンナップ処理
    # userテーブルのレコードを削除する
    User.query.delete()

    # user_imageテーブルのレコードを削除する
    UserImage.query.delete()

    # user_image_tagsテーブルのレコードを削除する
    UserImageTag.query.delete()

    # テスト用の画像アップロードディレクトリを削除する
    shutil.rmtree(app.config["UPLOAD_FOLDER"])

    db.session.commit()


# Flaskのテストクライアントを返すフィクスチャ関数を作成する
@pytest.fixture
def client(fixture_app):
    # Flaskのテスト用クライアントを返す
    return fixture_app.test_client()
