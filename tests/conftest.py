import pytest
from flask_login import login_user

from hktm import create_app, db
from hktm.models import User

@pytest.fixture(scope='session')
def test_client():
    flask_app = create_app('test.cfg')
    #flask_app.response_class = JSONResponse

    testing_client = flask_app.test_client(use_cookies=True)
    with flask_app.app_context():
        yield testing_client


@pytest.fixture(scope='session')
def init_database():
    db.create_all()

    db.session.commit()

    yield db

    db.drop_all()


@pytest.fixture()
def existing_user():
    user = User('testuser@gmail.com','password')
    user.grades = '1'

    db.session.add(user)
    db.session.commit()

@pytest.fixture(scope='session')
def authenticated_request(test_client):
    user = User('testuser@gmail.com','password')
    user.grades = '1'

    db.session.add(user)
    db.session.commit()

    with flask_app.test_request_context():
        yield login_user(User('testuser@gmail.com','password'))
