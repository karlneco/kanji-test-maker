from flask import url_for
from hktm import db
from hktm.models import User

def login(client,username,password):
    return client.post('/',data=dict(username=username,password=password), follow_redirects=True)

def logout(client):
    return client.get('/users/logout',follow_redirects=True)


def test_index_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert '補習校漢字テスト'.encode('utf-8') in response.data
    assert b'Log In' in response.data
    assert b'Register' in response.data

def test_valid_registration(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to (POST)
    THEN check the response is valid and the user is logged in
    """
    response = test_client.post('/users/register',
                                data=dict(email='testuser@gmail.com',
                                          password='password',
                                          password_confirm='password'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'Account created, please wait for a confirmation' in response.data
    user = User.query.filter_by(email='testuser@gmail.com').first()
    assert isinstance(user, User)
    assert user.grades == 'none'

def test_duplicate_registration(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to (POST)
    THEN check the response is valid and the user is logged in
    """
    response = test_client.post('/users/register',
                                data=dict(email='testuser@gmail.com',
                                          password='password',
                                          password_confirm='password'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'Account created, please wait for a confirmation' in response.data

    response = test_client.post('/users/register',
                                data=dict(email='testuser@gmail.com',
                                          password='password',
                                          password_confirm='password'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'This email is already registered' in response.data

def test_user_login(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/users/login or / (index) page is posted to (POST) with valid creds
    THEN login the user
    """

    user = User('testuser@gmail.com','password')
    user.grades = '1'  # a valid user needs a grade(s)
    db.session.add(user)
    db.session.commit()

    response = test_client.post('/',
                                data=dict(email='testuser@gmail.com',
                                          password='password'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'Login Successful' in response.data

def test_user_home(test_client, init_database, existing_user):
    """
    GIVEN a Flask application
    WHEN the '/users/login or / (index) page is posted to (POST) with valid creds
    THEN login the user
    """

    from flask_login import login_user,current_user

    # log in the user
    login(test_client,'testuser@gmail.com','password')
    login_user(User('testuser@gmail.com','password'))
    assert current_user.email == 'testuser@gmail.com'
    # try to get home
    response = c.get('/home',follow_redirects=True)
    assert response.status_code == 200
    #assert 0
    assert '新規作成または、'.encode('utf-8') in response.data



###############################################################################
# to see full response use try block to intercept the assetion
    # try:
    # make asserts here
    # except AssertionError as e:
    #     raise ResponseAssertionError(e, response)
    #
class ResponseAssertionError(AssertionError):
    def __init__(self, e, response):
        response_dump = "\n +  where full response was:\n" \
                        "HTTP/1.1 {}\n" \
                        "{}{}\n".format(response.status, response.headers, response.data)

        self.args = (e.args[0] + response_dump,)
