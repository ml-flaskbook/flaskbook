from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class SignUpForm(FlaskForm):
    username = StringField(
        "ユーザー名",
        validators=[
            DataRequired("ユーザ名は必須です。"),
            Length(1, 30, "30文字以内で入力してください。"),
        ],
    )
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Email("メールアドレスの形式で入力してください。"),
        ],
    )
    password = PasswordField("パスワード", validators=[DataRequired("パスワードは必須です。")])
    submit = SubmitField("新規登録")


class LoginForm(FlaskForm):
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Email("メールアドレスの形式で入力してください。"),
        ],
    )
    password = PasswordField("パスワード", validators=[DataRequired("パスワードは必須です。")])
    submit = SubmitField("ログイン")
