import pytest

from flask_login import login_user, login_manager, LoginManager

from hktm import create_app, db
from hktm.models import User, Lesson, LessonMaterial, MaterialType


@pytest.fixture()
def app():
    app = create_app('test.cfg')
    return app

@pytest.fixture()
def auth_user(app):
    @app.login_manager.request_loader
    def load_user_from_request(request):
        return User.query.first()

@pytest.fixture(scope='module')
def test_client():
    app = create_app('test.cfg')

    client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture()
def init_database():
    db.create_all()

    db.session.commit()

    yield db

    db.drop_all()

@pytest.fixture()
def add_data(init_database):
    material_type1 = MaterialType('KJTS','Kanji Test','Instruction for Kanji Test')
    material_type2 = MaterialType('TRCP','Tracing','Instruction for Tracing')
    material_type3 = MaterialType('KJWR','Kanji Writing','Instruction for Kanji Writing')
    material_type4 = MaterialType('KJRD','Kanji Reading','Instruction for Kanji Reading')
    material_type5 = MaterialType('NWRD','New Reading','Instruction for New Reading')
    material_type6 = MaterialType('KT36','Kanji Test 3-6','Instruction for Kanji Test grades 3-6')

    user1 = User('user1@gmail.com','password')
    user1.grades = '1'

    user2 = User('user26@gmail.com','password')
    user2.grades = '2,6'

    user3 = User('userempty@gmail.com','password')
    user3.grades = '3'

    user4 = User('usernoteset@gmail.com','password')


    userAdmin = User('admin@hoshuko.com','password')
    userAdmin.grades = 'A123456789'

    lesson11 = Lesson('Grade 1 - Lesson 1','1')
    lesson12 = Lesson('Grade 1 - Lesson 2','1')
    lesson21 = Lesson('Grade 2 - Lesson 1','2')
    lesson22 = Lesson('Grade 2 - Lesson 2','2')
    lesson61 = Lesson('Grade 6 - Lesson 1','6')



    db.session.add_all([material_type1,material_type2,material_type3,material_type4,material_type5,material_type6])
    db.session.add_all([user1, user2, user3, user4, userAdmin])
    db.session.add_all([lesson11, lesson12, lesson21, lesson22, lesson61])

    db.session.commit()

    lesson_mat_11_1 = LessonMaterial('Lesson 1 Material 1','something',lesson11.id,'KJTS')

    db.session.add(lesson_mat_11_1)
    db.session.commit()


@pytest.fixture()
def existing_user():
    user = User('testuser@gmail.com','password')
    user.grades = '1'

    db.session.add(user)
    db.session.commit()

@pytest.fixture
def authenticated_request(test_client):
    user = User('testuser@gmail.com','password')
    user.grades = '1'

    db.session.add(user)
    db.session.commit()

    # with flask_app.test_request_context():
    #     yield login_user(User('testuser@gmail.com','password'))



######################################## fix for Live_server fixture and windows
# @pytest.fixture(scope="session")
# def flask_port():
#     ## Ask OS for a free port.
#     #
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind(("", 0))
#         addr = s.getsockname()
#         port = addr[1]
#         return port
#
# @pytest.fixture(scope="session", autouse=True)
# def live_server(flask_port):
#     env = os.environ.copy()
#     env["FLASK_APP"] = "main.py"
#     server = subprocess.Popen(['flask', 'run', '--port', str(flask_port)], env=env)
#     try:
#         yield server
#     finally:
#         server.terminate()
