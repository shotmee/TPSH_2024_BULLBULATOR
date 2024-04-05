import sqlite3
import os
from UserLogin import UserLogin
from flask import Flask, render_template, request, flash, g, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from FDataBase import FDataBase
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user
from templates.forms import LoginForm
from sql import *

DATABASE = '/tmp/dbase.db'
DEBUG = True
MAX_CONTENT_LENGTH = 1024 * 1024

SECRET_KEY = os.urandom(32)

HOST_NAME = "localhost"
HOST_PORT = 80
app = Flask(__name__, static_folder='static')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config.update(dict(DATABASE=os.path.join(app.root_path,'dbase.db')))

Session = sessionmaker(bind=engine)
session = Session()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

@app.route('/redirect', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('dbase.db')
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()

        conn.close()

        if user:
            return redirect('/profile')
        else:
            return "Неверное имя пользователя или пароль"

    return render_template('log_page.html')

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None
@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


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
    return redirect('/<int:teacher_id>')

@app.route("/")
def main():
    return render_template('main_page.html')

@app.route("/ShowTeachers")
def index():
    teachers = session.query(Teacher).all()
    return render_template('teachers_page.html', teachers=teachers)

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/<int:teacher_id>')
def view_teacher(teacher_id):
    teacher = session.query(Teacher).get(teacher_id)
    return render_template('teacher.html', teacher=teacher)

@app.route("/profile")
#@login_required
def profile():
    return render_template("cabinet.html", title="Профиль")
#    return render_template("cabinet.html", menu=dbase.getMenu(), title="Профиль")

@app.route("/<int:lesson_id>")
def lesson():
    return render_template("lessons.html", title="Оценка занятия")

if __name__ == "__main__":
    app.run(debug=True)
