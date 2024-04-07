from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin 

db = SQLAlchemy()

#Модель профиля
class profiles(UserMixin, db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150))
    middlename = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))

    
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'), nullable=False)
    grade = db.relationship('grades', backref='students')

    def __init__(self, firstname=None, middlename=None, lastname=None, username=None, password=None, grade_id=None):
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.username = username
        self.password = password
        self.grade_id = grade_id
    
    def check_password(self, another_password):
        if self.password == another_password:
            return True
        return False
    
    def __repr__(self):
        return '<profiles %r>'%(self.name)

# Модель класса учебы (готов)
class grades(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)
    symbol = db.Column(db.String(2))

    def __init__(self, number=None, symbol=None):
        self.number = number
        self.symbol = symbol
    
    def __repr__(self):
        return '<grades %r>'%(self.name)

# Модель урока (готово)
class lessons(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name=None):
        self.name = name
    
    def __repr__(self):
        return '<lessons %r>'%(self.name)

# Модель дня недели (day_of_the_week) (готово)
class daysweek(db.Model):
    __tablename__ = 'daysweek'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<daysweek %r>'%(self.name)

# Модель ячейки в расписании в дне недели (time_of_the_lessons) (готово)
class timelessons(db.Model):
    __tablename__ = 'timelessons'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)

    day_id = db.Column(db.Integer, db.ForeignKey('daysweek.id'), nullable=False)
    day = db.relationship('daysweek', backref='timelessons')

    def __init__(self, number=None, day_id=None):
        self.number = number
        self.day = day_id

    def __repr__(self):
        return '<timelessons %r>'%(self.name)
    
# Модель преподавателя (готов)
class teachers(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(150))

    def __init__(self, fullName=None):
        self.fullName = fullName
    
    def __repr__(self):
        return '<teachers %r>'%(self.name)

# Модель ячейки расписания (готов)
class cellsschedule(db.Model):
    __tablename__ = 'cellsschedule'
    id = db.Column(db.Integer, primary_key=True)
    lesson_name = db.Column(db.String(20), db.ForeignKey('lessons.name'), nullable=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    teacher = db.relationship('teachers', backref='lessons')

    grades_id = db.Column(db.Integer, db.ForeignKey('grades.id'), nullable=False)
    grade = db.relationship('grades', backref='lessons')

    number_id = db.Column(db.Integer, db.ForeignKey('timelessons.id'), nullable=False)
    number = db.Column(db.Integer, db.ForeignKey('timelessons.number'), nullable=False)

    day_name = db.Column(db.Integer, db.ForeignKey('daysweek.name'), nullable=False)
    day = db.relationship('daysweek', backref='lessons')

    def __init__(self, number=None, day_id=None):
        self.number = number
        self.day = day_id

    def __repr__(self):
        return '<cellsschedule %r>'%(self.name)

# Модель одного отзыва
class feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)

    cellsschedule_id = db.Column(db.Integer, db.ForeignKey('cellsschedule.id'), nullable=False)
    cellschedule = db.relationship('cellsschedule', backref='feedback')

    main_rating = db.Column(db.Integer)
    availability = db.Column(db.String(300))
    objectivity = db.Column(db.String(300))
    creative = db.Column(db.String(300))
    depth = db.Column(db.String(300))
    humor = db.Column(db.String(300))
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    profile = db.relationship('profiles', backref='feedbacks')

    def __init__(self, cellsschedule_id=None, main_rating=None,availability=None, objectivity=None,
                 creative=None, depth=None, humor=None, profile_id=None):
        self.cellsschedule_id = cellsschedule_id
        self.main_rating = main_rating
        self.availability = availability
        self.objectivity = objectivity
        self.creative = creative
        self.depth = depth
        self.humor = humor
        self.profile_id = profile_id
    
    def __repr__(self):
        return '<feedback %r>'%(self.name)
    
class feedback_for_teacher(db.Model):
    __tablename__ = 'feedback_for_teacher'
    id = db.Column(db.Integer, primary_key=True)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    teacher = db.relationship('teachers', backref='feedback')

    main_rating = db.Column(db.Integer)
    availability = db.Column(db.String(300))
    objectivity = db.Column(db.String(300))
    creative = db.Column(db.String(300))
    depth = db.Column(db.String(300))
    humor = db.Column(db.String(300))
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    profile = db.relationship('profiles', backref='feedbacks_teachers')

    def __init__(self, cellsschedule_id=None, main_rating=None,availability=None, objectivity=None,
                 creative=None, depth=None, humor=None, profile_id=None):
        self.cellsschedule_id = cellsschedule_id
        self.main_rating = main_rating
        self.availability = availability
        self.objectivity = objectivity
        self.creative = creative
        self.depth = depth
        self.humor = humor
        self.profile_id = profile_id
    
    def __repr__(self):
        return '<feedback %r>'%(self.name)