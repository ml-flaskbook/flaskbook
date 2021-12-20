import pytest
from api.run import create_app, db


@pytest.fixture
def app():
    """
    テスト用のデータベースを作成
    """
    app = create_app()
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    yield app

    db.session.remove()
    db.drop_all()
    app_context.pop()


@pytest.fixture
def client(app):
    """
    テスト用のrequestオブジェクトを作成
    """
    return app.test_client()
