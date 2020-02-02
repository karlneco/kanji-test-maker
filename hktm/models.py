from hktm import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Lesson(db.Model):
    __tablename__ = 'lesson'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    date = db.Column(db.Text)
    grade = db.Column(db.Integer)
    comments = db.Column(db.Text)

    # one-to-many; one lesson may have many materials
    lesson_materials = db.relationship('LessonMaterial', backref='lesson_material', lazy='dynamic')

    def __init__(self, name, grade):
        self.name=name
        self.grade=grade


    def __repr__(self):
        return f'{self.name} is a grade {self.grade} lesson with {lesson_materials.length}'

class MaterialType(db.Model):
    __tablename__ = 'material_type'
    code = db.Column(db.Text,primary_key=True)
    name = db.Column(db.Text)
    instructions = db.Column(db.Text)
    custom_template = db.Column(db.Boolean)

    def __init__(self,code,name,insturctions):
        self.code=code
        self.name=name
        self.instructions=insturctions

    def __repr__(self):
        return f'{self.name} is a material identified by code {self.code}'

class LessonMaterial(db.Model):
    __tablename__ = 'lesson_material'
    id = db.Column(db.Integer,primary_key=True)

    name = db.Column(db.Text) # this can indicate the worksheet name and number
    content = db.Column(db.Text)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    material_code = db.Column(db.Text, db.ForeignKey('material_type.code'))
    material = db.relationship("MaterialType")



    def __init__(self,name,content,lesson_id,material_code):
        self.name=name
        self.content=content
        self.lesson_id = lesson_id
        self.material_code = material_code

    def __repr__(self):
        return f'this is the worksheet {self.name} for the lesson'


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))
    grades = db.Column(db.String, nullable=False, default='none')
    password_hash = db.Column(db.String(128))


    def __init__(self,email,password):
        self.email = email
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.email
