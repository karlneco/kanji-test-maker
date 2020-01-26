from flask import url_for
import requests

from hktm import db
from hktm.models import User

def test_new_good_lesson(client,auth_user,init_database,authenticated_request):
    """
    GIVEN a Flask application
    WHEN the user creates a valid new lesson
    THEN inform them and go to the edit screen
    """
    response = client.post(url_for('root.index'),data=dict(email='testuser@gmail.com',password='password'))
    # try to get home
    response = client.post(url_for('lessons.add'),data=dict(name='test lesson 1',grade='1'),follow_redirects=True)
    assert response.status_code == 200
    assert b'New Lesson Created' in response.data #user informed
    assert '編集したいプリントを選べます'.encode('utf-8') in response.data #at the edit screen

def test_new_lesson_no_name(client,auth_user,init_database,authenticated_request):
    """
    GIVEN a Flask application
    WHEN the user tries to add a lesson with no 'name'
    THEN display an error message
    """
    response = client.post(url_for('root.index'),data=dict(email='testuser@gmail.com',password='password'))
    # try to get home
    response = client.post(url_for('lessons.add'),data=dict(name='',grade='1'),follow_redirects=True)
    assert response.status_code == 200
    assert b'required' in response.data #part of error message

def test_lesson_list_empty(client, auth_user, init_database, add_data):
    """
    GIVEN a Flask application
    WHEN the asks for a list of lessons but the user doesnt have any
    THEN display an empty list
    """
    response = client.post(url_for('root.index'),data=dict(email='userempty@gmail.com',password='password'))
    # try to get home
    response = client.get(url_for('lessons.list'))
    assert response.status_code == 200
    #assert 0
    assert b'<a class="list-group-item ' not in response.data #part of the table with lessons

def test_lesson_list_1grade(client, auth_user, init_database, add_data):
    """
    GIVEN a Flask application
    WHEN the asks for a list of lessons the user has 2 grades
    THEN display an empty list
    """
    response = client.post(url_for('root.index'),data=dict(email='user1@gmail.com',password='password'))
    # try to get home
    response = client.get(url_for('lessons.list'))
    assert response.status_code == 200
    #assert 0
    assert b'Grade 1 ' in response.data #part of the table with lessons for grade 1
    assert b'Grade 2 ' not in response.data #part of the table with lessons for grade 6
    assert b'Grade 6 ' not in response.data #part of the table with lessons for grade 6

def test_lesson_list_2grades(client, auth_user, init_database, add_data):
    """
    GIVEN a Flask application
    WHEN the asks for a list of lessons the user has 2 grades
    THEN display an empty list
    """
    response = client.post(url_for('root.index'),data=dict(email='user26@gmail.com',password='password'))
    # try to get home
    response = client.get(url_for('lessons.list'))
    assert response.status_code == 200
    #assert 0
    assert b'Grade 2 ' in response.data #part of the table with lessons for grade 2
    assert b'Grade 6 ' in response.data #part of the table with lessons for grade 6

def test_lesson_list_admin(client, auth_user, init_database, add_data):
    """
    GIVEN a Flask application
    WHEN the asks for a list of lessons the user has 2 grades
    THEN display an empty list
    """
    response = client.post(url_for('root.index'),data=dict(email='admin@hoshuko.com',password='password'))
    # try to get home
    response = client.get(url_for('lessons.list'))
    assert response.status_code == 200
    #assert 0
    assert b'Grade 1 ' in response.data #part of the table with lessons for grade 2
    assert b'Grade 2 ' in response.data #part of the table with lessons for grade 2
    assert b'Grade 6 ' in response.data #part of the table with lessons for grade 6

#TODO: as this is testing input form a drop down its lower priority for now
#def test_new_bad_lesson(client,auth_user,init_database,authenticated_request):
    # """
    # GIVEN a Flask application
    # WHEN the '/users/login or / (index) page is posted to (POST) with valid creds
    # THEN login the user
    # """
    # response = client.post(url_for('root.index'),data=dict(username='testuser@gmail.com',password='password'))
    #
    # # add a lesson thats not in the users class - this would have to be a hack as its a drop down
    # response = client.post(url_for('lessons.add'),data=dict(name='test lesson 1',grade='99'),follow_redirects=True)
    # assert response.status_code == 200
    # assert b'New Lesson Created' not in response.data
    # assert b'You cannot add lessons to that grade' in response.data
