from flask import render_template, request, redirect, session, url_for, abort, flash
from flask_login import login_required, login_user, current_user

from app import app, db, socketio
from .projects import Project, Comment
from .auth import User, permission_required


"""
Projects
"""

@app.route('/')
@login_required
def index():
	if current_user.role == 'project_manager':
		projects = Project.objects()
	elif current_user.role == 'engineer':
		projects = Project.objects(engineers__in=[current_user.id])
	return render_template('index.html', title='Home', projects=projects)


@app.route('/projects/create', methods=['GET','POST'])
@login_required
@permission_required('project_manager')
def create_project():
	if request.method == 'POST':
		title = request.form['title']
		engineers = request.form.getlist('engineers')
		users = [User.objects(id=engineer).first() for engineer in engineers]
		Project(title=title, engineers=users).save()
		return redirect('/')
	users = User.objects(role='engineer')
	return render_template('projects/create.html', users=users)


@app.route('/projects/<id>', methods=['GET', 'POST'])
@login_required
def project(id):
	project = Project.objects(id=id)
	if current_user.role == 'project_manager':
		project = project.first()
	elif current_user.role == 'engineer':
		project = project(engineers__in=[current_user.id]).first()
	return render_template('projects/project.html', project=project)


@socketio.on('comment', namespace='/comment')
def post_comment(data):
	project = Project.objects(id=data['id'])
	comment = Comment(text=data['text'], by=current_user.id)
	project.update_one(push__comments=comment)
	emit_data = {
		'project_id': data['id'],
		'text': comment.text,
		'by': comment.by.username
	}
	socketio.emit('comment', emit_data, namespace='/comment')
	socketio.emit('notification', emit_data, namespace='/')


"""
Authentication
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		user = User.objects(username=request.form.get('username')).first()
		if user and user.check_password(request.form.get('password')):
			login_user(user)
			return redirect(url_for('index'))
		flash('Invalid login credentials.')
	return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		user = User.objects(username=request.form.get('username')).first()
		if not user:
			new_user = User(username=request.form.get('username'))
			new_user.set_password(password=request.form.get('password'))
			new_user.role = request.form.get('role')
			new_user.save()
			login_user(new_user)
			return redirect(url_for('index'))

		flash('The username is already exists.')
	return render_template('auth/register.html')


@app.route('/logout')
@login_required
def logout():
	session.clear()
	return redirect('/')
