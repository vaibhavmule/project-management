from flask import render_template, request, redirect, session, url_for
from app import app, db, socketio, login_required
from bson import ObjectId
from passlib.hash import pbkdf2_sha256

from .projects import Project, Comment


@app.route('/')
@login_required
def index():
	projects = Project.objects.all()
	return render_template('index.html', title='Home', projects=projects)


@app.route('/projects/create', methods=['GET','POST'])
@login_required
def create_project():
	if request.method == 'POST':
		title = request.form['title']
		Project(title=title).save()
		return redirect('/')
	return render_template('projects/create.html')


@app.route('/projects/<id>', methods=['GET', 'POST'])
@login_required
def project(id):
	project = Project.objects.get(id=id)
	return render_template('projects/project.html', project=project)


@socketio.on('comment', namespace='/comment')
def post_comment(data):
	project = Project.objects(id=data['id'])
	comment = Comment(text=data['text'])
	project.update_one(push__comments=comment)
	socketio.emit('comment', data, namespace='/comment')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		user = db.users.find_one({
		  "username": request.form.get('username')
		})
		if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
			session['username'] = request.form.get('username')
			return redirect(url_for('index'))
	return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		users = db.users
		exists = users.find_one({'username' : request.form['username']})
		if not exists:
			users.insert_one({
				'username' : request.form['username'],
				'password' : pbkdf2_sha256.encrypt(request.form['password']),
				'role': int(request.form['role'])
			})
			session['username'] = request.form['username']
			return redirect(url_for('index'))

		return "The username already exists"
	return render_template('auth/register.html')


@app.route('/logout')
@login_required
def logout():
	session.clear()
	return redirect('/')
