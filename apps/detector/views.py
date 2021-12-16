from apps.app import db
from apps.crud.models import User
from apps.detector.models import UserImage
from flask import Blueprint, render_template

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
