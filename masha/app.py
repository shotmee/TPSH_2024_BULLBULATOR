from flask import Flask, render_template
from sqlalchemy.orm import sessionmaker 
from sql import *

app = Flask(__name__)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    teachers = session.query(Teacher).all()
    return render_template('index.html', teachers=teachers)

@app.route('/<int:teacher_id>')
def view_teacher(teacher_id):
    teacher = session.query(Teacher).get(teacher_id)
    return render_template('teacher.html', teacher=teacher)


if __name__ == '__main__':
    app.debug = True
    app.run(port=4996)
