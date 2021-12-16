import uuid
from pathlib import Path

from apps.app import db
from apps.crud.models import User

# UploadImageFormをimportする
from apps.detector.forms import UploadImageForm
from apps.detector.models import UserImage
from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)

# login_required, current_userをimportする
from flask_login import current_user, login_required

# template_folderを指定する（staticは指定しない）
dt = Blueprint("detector", __name__, template_folder="templates")


# dtアプリケーションを使ってエンドポイントを作成する
@dt.route("/")
def index():
    # UserとUserImageをJoinして画像一覧を取得する
    user_images = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .all()
    )
    return render_template("detector/index.html", user_images=user_images)


@dt.route("/images/<path:filename>")
def image_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@dt.route("/upload", methods=["GET", "POST"])
# ログイン必須とする
@login_required
def upload_image():
    # UploadImageFormを利用してバリデーションをする
    form = UploadImageForm()
    if form.validate_on_submit():
        # アップロードされた画像ファイルを取得する
        file = form.image.data

        # ファイルのファイル名と拡張子を取得し、ファイル名をuuidに変換する
        ext = Path(file.filename).suffix
        image_uuid_file_name = str(uuid.uuid4()) + ext

        # 画像を保存する
        image_path = Path(current_app.config["UPLOAD_FOLDER"], image_uuid_file_name)
        file.save(image_path)

        # DBに保存する
        user_image = UserImage(user_id=current_user.id, image_path=image_uuid_file_name)
        db.session.add(user_image)
        db.session.commit()

        return redirect(url_for("detector.index"))
    return render_template("detector/upload.html", form=form)
