from datetime import datetime

from apps.app import db


class UserImage(db.Model):
    __tablename__ = "user_images"
    id = db.Column(db.Integer, primary_key=True)
    # user_idはusersテーブルのidカラムを外部キーとして設定する
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    image_path = db.Column(db.String)
    is_detected = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class UserImageTag(db.Model):
    # テーブル名を指定する
    __tablename__ = "user_image_tags"
    id = db.Column(db.Integer, primary_key=True)
    # user_image_idはuser_imagesテーブルのidカラムの外部キーとして設定する
    user_image_id = db.Column(db.String, db.ForeignKey("user_images.id"))
    tag_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
