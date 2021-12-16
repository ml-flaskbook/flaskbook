from pathlib import Path

from apps.detector.models import UserImage
from flask.helpers import get_root_path
from werkzeug.datastructures import FileStorage


def test_index(client):
    rv = client.get("/")
    assert "ログイン" in rv.data.decode()
    assert "画像新規登録" in rv.data.decode()


def signup(client, username, email, password):
    """サインアップする"""
    data = dict(username=username, email=email, password=password)
    return client.post("/auth/signup", data=data, follow_redirects=True)


def test_index_signup(client):
    """サインアップを実行する"""
    rv = signup(client, "admin", "flaskbook@example.com", "password")
    assert "admin" in rv.data.decode()
    rv = client.get("/")
    assert "ログアウト" in rv.data.decode()
    assert "画像新規登録" in rv.data.decode()


def test_upload_no_auth(client):
    rv = client.get("/upload", follow_redirects=True)
    # 画像アップロード画面にはアクセスできない
    assert "アップロード" not in rv.data.decode()
    # ログイン画面へリダイレクトされる
    assert "メールアドレス" in rv.data.decode()
    assert "パスワード" in rv.data.decode()


def test_upload_signup_get(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    rv = client.get("/upload")
    assert "アップロード" in rv.data.decode()


def upload_image(client, image_path):
    """画像をアップロードする"""
    image = Path(get_root_path("tests"), image_path)
    test_file = (
        FileStorage(
            stream=open(image, "rb"),
            filename=Path(image_path).name,
            content_type="multipart/form-data",
        ),
    )
    data = dict(
        image=test_file,
    )
    return client.post("/upload", data=data, follow_redirects=True)


def test_upload_signup_post_validate(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    rv = upload_image(client, "detector/testdata/test_invalid_file.txt")
    assert "サポートされていない画像形式です。" in rv.data.decode()


def test_upload_signup_post(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    rv = upload_image(client, "detector/testdata/test_valid_image.jpg")
    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()


def test_detect_no_user_image(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    upload_image(client, "detector/testdata/test_valid_image.jpg")
    # 存在しないIDを指定する
    rv = client.post("/detect/notexistid", follow_redirects=True)
    assert "物体検知対象の画像が存在しません。" in rv.data.decode()


def test_detect(client):
    # サインアップする
    signup(client, "admin", "flaskbook@example.com", "password")

    # 画像をアップロードする
    upload_image(client, "detector/testdata/test_valid_image.jpg")
    user_image = UserImage.query.first()

    # 物体検知を実行する
    rv = client.post(f"/detect/{user_image.id}", follow_redirects=True)
    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()
    assert "dog" in rv.data.decode()


def test_detect_search(client):
    # サインアップする
    signup(client, "admin", "flaskbook@example.com", "password")

    # 画像をアップロードする
    upload_image(client, "detector/testdata/test_valid_image.jpg")

    user_image = UserImage.query.first()
    # 物体検知する
    client.post(f"/detect/{user_image.id}", follow_redirects=True)

    # dogワードで検索する
    rv = client.get("/images/search?search=dog")

    # dogタグの画像があることを確認する
    assert user_image.image_path in rv.data.decode()

    # dogタグがあることを確認する
    assert "dog" in rv.data.decode()

    # testワードで検索する
    rv = client.get("/images/search?search=test")

    # dogタグの画像がないことを確認する
    assert user_image.image_path not in rv.data.decode()

    # dogタグがないことを確認する
    assert "dog" not in rv.data.decode()


def test_delete(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    upload_image(client, "detector/testdata/test_valid_image.jpg")
    user_image = UserImage.query.first()
    image_path = user_image.image_path
    rv = client.post(f"/images/delete/{user_image.id}", follow_redirects=True)
    assert image_path not in rv.data.decode()


def test_custom_error(client):
    rv = client.get("/notfound")
    assert "404 Not Found" in rv.data.decode()
