from UserLogin import UserLogin
from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from templates.forms import LoginForm, RegisterForm
from sql import *

app = Flask(__name__)

Session = sessionmaker(bind=engine)
session = Session()

@app.route("/")
@app.route("/ShowTeachers")
def index():
    teachers = session.query(Teacher).all()
    return render_template('index.html', teachers=teachers)

@app.route('/<int:teacher_id>')
def view_teacher(teacher_id):
    teacher = session.query(Teacher).get(teacher_id)
    return render_template('teacher.html', teacher=teacher)

@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        if user and check_password_hash(user['psw'], form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html", menu=dbase.getMenu(), title="Авторизация", form=form)

@app.route('/signin', methods=["POST", "GET"])
def signin():
    form = RegisterForm()
    if form.validate_on_submit():
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(form.name.data, form.email.data, hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")

    return render_template("register.html", menu=dbase.getMenu(), title="Регистрация", form=form)


@app.route("/profile")
def profile():
    return ""


@app.route("/teachers/new", methods=['GET', 'POST'])
def newTeacher():
    if request.method == 'POST':
        newTeacher = Teacher(name=request.form['fio'])
        session.add(newTeacher)
        session.commit()
        return redirect(url_for('showTeachers'))
    else:
        return render_template('newTeacher.html')

@app.route("/teachers/<int:teachers_id>/edit", methods=['POST', 'GET'])
def editTeacher(teacher_id):
    editedTeacher = session.query(Teacher).filtered_by(id=teacher_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedTeacher.title = request.form['name']
            return redirect(url_for('showTeachers'))
    else:
        return render_template('editTeacher.html', teacher=editedTeacher)


if __name__ == "__main__":
    app.run(debug=True)
