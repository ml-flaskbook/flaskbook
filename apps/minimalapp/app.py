import logging
import os

from email_validator import EmailNotValidError, validate_email
from flask import (
    Flask,
    current_app,
    flash,
    g,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

# Flaskクラスをインスタンス化する
app = Flask(__name__)

# SECRET_KEYを追加する
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"

# ログレベルを設定する
app.logger.setLevel(logging.DEBUG)

# リダイレクトを中断しないようにする
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# Mailクラスのコンフィグを追加する
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# DebugToolbarExtensionにアプリケーションをセットする
toolbar = DebugToolbarExtension(app)

# flask-mail拡張を登録する
mail = Mail(app)


# URLと実行する関数をマッピングする
@app.route("/")
def index():
    return "Hello, Flaskbook!"


@app.route("/hello/<name>", methods=["GET"], endpoint="hello-endpoint")
def hello(name):
    return f"Hello, {name}"


# show_nameエンドポイントを作成する
@app.route("/name/<name>")
def show_name(name):
    # 変数をテンプレートエンジンに渡す
    return render_template("index.html", name=name)


# Flask2からは@app.get("/hello")、@app.post("/hello")と記述することが可能
# @app.get("/hello")
# @app.post("/hello")
# def hello():
#   return "Hello, World!"


with app.test_request_context():
    # /
    print(url_for("index"))
    # /hello/world
    print(url_for("hello-endpoint", name="world"))
    # /name/ichiro?page=ichiro
    print(url_for("show_name", name="ichiro", page="1"))


# ここで呼び出すとエラーとなる
# print(current_app)

# アプリケーションコンテキストを取得してスタックへpushする
ctx = app.app_context()
ctx.push()

# current_appにアクセスが可能になる
print(current_app.name)
# >> apps.minimalapp.app

# グローバルなテンポラリ領域に値を設定する
g.connection = "connection"
print(g.connection)
# >> connection

with app.test_request_context("/users?updated=true"):
    # trueが出力される
    print(request.args.get("updated"))


@app.route("/contact")
def contact():
    # レスポンスオブジェクトを取得する
    response = make_response(render_template("contact.html"))

    # クッキーを設定する
    response.set_cookie("flaskbook key", "flaskbook value")

    # セッションを設定する
    session["username"] = "ichiro"

    # レスポンスオブジェクトを返す
    return response


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # form属性を使ってフォームの値を取得する
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # 入力チェック
        is_valid = True
        if not username:
            flash("ユーザ名は必須です")
            is_valid = False

        if not email:
            flash("メールアドレスは必須です")
        is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False

        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        # メールを送る
        send_email(
            email,
            "問い合わせありがとうございました。",
            "contact_mail",
            username=username,
            description=description,
        )

        # 問い合わせ完了エンドポイントへリダイレクトする
        flash("問い合わせありがとうございました。")

        # contactエンドポイントへリダイレクトする
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")


app.logger.critical("fatal error")
app.logger.error("error")
app.logger.warning("warning")
app.logger.info("info")
app.logger.debug("debug")


def send_email(to, subject, template, **kwargs):
    """メールを送信する関数"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
