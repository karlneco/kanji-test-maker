from hktm import db
# As a question can be on many tests and a test will have many questions
#    we will set up a many-to-many relation ship here ab use a "helper table"
#    as in the SQLAlchemy docs

class Lesson(db.Model):
    __tablename__ = 'lesson'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    date = db.Column(db.Text)
    grade = db.Column(db.Integer)
    comments = db.Column(db.Text)

    # one-to-many; one lesson may have many materials
    lesson_materials = db.relationship('LessonMaterial', backref='lesson_material', lazy='dynamic')

    def __init__(self,name):
        self.name=name


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
