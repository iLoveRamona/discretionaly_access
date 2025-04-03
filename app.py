READ = 0b00001      # 1
WRITE = 0b00010     # 2
EXECUTE = 0b00100   # 4
TAG = 0b01000       # 8
OWN = 0b10000       # 16


RX = READ | EXECUTE  # 5
RWXT = READ | WRITE | EXECUTE | TAG  # 15
RWXTO = READ | WRITE | EXECUTE | TAG | OWN  # 31



import os


from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import db
from models import User, Task, UserTask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ctf:ctf@localhost:5432/db_ctf' 
app.secret_key = 'cocacola'
db.init_app(app)

@app.route('/')
def index():
    if 'username' in session:
        user = User.query.filter_by(user=session['username']).first()
        user_tasks = UserTask.query.filter_by(user_id=user.userid).all()
        readable_task_ids = [user_task.task_id for user_task in user_tasks if user_task.has_permission(READ)]
        tasks = Task.query.filter(Task.task_id.in_(readable_task_ids)).all()
        return render_template('index.html', username=session['username'], tasks=tasks)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(user=username).first()
        if user and user.password == password:
            session['username'] = username
            flash('Успешный вход!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль.', 'danger')
    return render_template('login.html')

@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    description_path = os.path.join(task.directory, 'description.txt')
    image_path = os.path.join(task.directory, 'image.png')
    image_path = "../" + image_path  
    print(description_path, image_path)
    if os.path.isfile(description_path):
        with open(description_path, 'r', encoding='utf-8') as file:
            description = file.read()
    else:
        description = "Файл не найден."
    return render_template('task_detail.html', task=task, description=description, image_path=image_path)


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
