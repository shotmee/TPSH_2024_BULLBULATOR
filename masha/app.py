import sqlite3
import os
# from UserLogin import UserLogin
from flask import Flask, render_template, request, g, redirect
# from FDataBase import FDataBase
from sql import db, profiles, teachers, grades, lessons, daysweek, timelessons, cellsschedule, feedback, feedback_for_teacher
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
# DATABASE = '/tmp/dbase.db'
# DEBUG = True
# MAX_CONTENT_LENGTH = 1024 * 1024

# SECRET_KEY = os.urandom(32)

# HOST_NAME = "localhost"
# HOST_PORT = 80
app = Flask(__name__, static_folder='static')
# app.config.from_object(__name__)
# app.config['SECRET_KEY'] = SECRET_KEY
# app.config.update(dict(DATABASE=os.path.join(app.root_path,'dbase.db')))
app.config.from_object('config')
db.init_app(app)

# Session = sessionmaker(bind=engine)
# session = Session()

with app.app_context():
    db.create_all()

login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
# login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(id):
    # print("load_user")
    return profiles.query.get(int(id))

@app.route('/redirect', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # conn = sqlite3.connect('dbase.db')
        # c = conn.cursor()

        # c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        # user = c.fetchone()

        # conn.close()

        user = profiles.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect('/profile')
        else:
            return "<p> color: red;'> Неверное имя пользователя или пароль </p>"

    return render_template('log_page.html')

# def connect_db():
#     conn = sqlite3.connect(app.config['DATABASE'])
#     conn.row_factory = sqlite3.Row
#     return conn

# def create_db():
#     """Вспомогательная функция для создания таблиц БД"""
#     db = connect_db()
#     with app.open_resource('sq_db.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#     db.close()

# def get_db():
#     '''Соединение с БД, если оно еще не установлено'''
#     if not hasattr(g, 'link_db'):
#         g.link_db = connect_db()
#     return g.link_db


# dbase = None
# @app.before_request
# def before_request():
#     """Установление соединения с БД перед выполнением запроса"""
#     global dbase
#     db = get_db()
#     dbase = FDataBase(db)


# @app.teardown_appcontext
# def close_db(error):
#     '''Закрываем соединение с БД, если оно было установлено'''
#     if hasattr(g, 'link_db'):
#         g.link_db.close()


@app.route('/redirect', methods=['GET'])
def redirect_page():
    return redirect('/login')

@app.route('/redirect1', methods=['GET'])
def redirect_page1():
    return redirect('/profile')

@app.route('/redirect2', methods=['GET'])
def redirect_page2():
    return redirect('/ShowTeachers')

@app.route('/redirect3', methods=['GET'])
def redirect_page3():
    return redirect('/schedule')

@app.route('/redirect4', methods=['GET'])
def redirect_page4():
    return redirect('/teacher_1')

@app.route("/")
def main():
    return render_template('main_page.html')

@app.route("/ShowTeachers")
@login_required
def index():
    ateachers = teachers.query.limit(10).all()
    return render_template('teachers_page.html', teachers=ateachers)

@app.route('/schedule')
@login_required
def schedule():
    return render_template('schedule.html')

@app.route('/teacher_1')
@login_required
def view_teacher():
    teacher_id=1
    teacher = teachers.query.filter_by(id=teacher_id).first()
    fullName = teacher.fullName

    lessons = db.session.query(lessons).join(cellsschedule).filter(cellsschedule.teacher_id == teacher_id).all()

    feedbacks_for_teachers_lessons = db.session.query(feedback).join(
        cellsschedule, cellsschedule.id == feedback.cellsschedule_id).join(
            teachers, teachers.id == cellsschedule.teacher_id).filter(
                teachers.id == teacher_id).all()
    
    feedbacks_for_teacher = feedbacks_for_teacher = db.session.query(
        feedback_for_teacher).join(
            teachers, teachers.id == feedback_for_teacher.teacher_id).filter(
                teachers.id == teacher_id).all()
    print(feedback_for_teacher)
    return render_template('teacher2.html', lesson= 'edfw', grades='sefw')


# @app.route('/<int:teacher_id>/feedback', methods=['GET', 'POST'])
# @login_required
# def view_teacher(teacher_id):
#     teacher = teachers.query.filter_by(teacher_id).first()
#     fullname = teacher.fullName


#     if request.method == 'POST':
#         main_rating = request.form['rating']
#         availability = request.form['availability']
#         objectivity = request.form['objectivity']
#         creative = request.form['creative']
#         depth = request.form['depth']
#         humor = request.form['humor']

#         profile_id = current_user.id

#         new_feedback = feedback_for_teacher(teacher_id, main_rating,availability, objectivity,
#                  creative, depth, humor, profile_id)
        
#         db.session.add(new_feedback)
#         db.session.commit()

#         return redirect('/<int:teacher_id>')
#     return render_template('teacher2.html', teacher=teacher)

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    firstname = current_user.firstname
    middlename = current_user.middlename
    lastname = current_user.lastname
    user_id = current_user.id

    if request.method == 'POST':
        user = profiles.query.get(user_id)
        if user:
            new_firstname = request.form['firstname']
            new_middlename = request.form['middlename']
            new_lastname = request.form['lastname']
            
            user.firstname = new_firstname
            user.middlename = new_middlename
            user.lastname = new_lastname
            db.session.commit()

    return render_template("cabinet.html", title="Профиль", firstname=firstname, middlename=middlename, lastname=lastname, user_id=user_id)
#    return render_template("cabinet.html", menu=dbase.getMenu(), title="Профиль")

@app.route("/<int:lesson_id>", methods=['GET', 'POST'])
@login_required
def lesson(cellsschedule_id):
    lesson = cellsschedule.query.get(cellsschedule_id)
    lessonName = lesson.lesson_name
    lessonDate = lesson.day_name
    lessonFullName = lessonName + ' ' + lessonDate

    if request.method == 'POST':
        main_rating = request.form['rating']
        availability = request.form['availability']
        objectivity = request.form['objectivity']
        creative = request.form['creative']
        depth = request.form['depth']
        humor = request.form['humor']

        profile_id = current_user.id

        new_feedback = feedback(cellsschedule_id, main_rating,availability, objectivity,
                 creative, depth, humor, profile_id)
        
        db.session.add(new_feedback)
        db.session.commit()

        return redirect('/schedule')
    return render_template("lessons.html", title="Оценка занятия")

if __name__ == "__main__":
    app.run(debug=True)

    