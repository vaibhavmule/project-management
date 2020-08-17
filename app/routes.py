from flask import render_template, request, redirect
from app import app, db, socketio, login_required
from bson import ObjectId


@app.route('/')
def index():
	projects = db.projects.find()
	return render_template('index.html', title='Home', projects=projects)


@app.route('/projects/create', methods=['GET','POST'])
def create_project():
	if request.method == 'POST':
		title = request.form['title']
		db.projects.insert_one({'title': title})
		return redirect('/')
	return render_template('create.html')


@app.route('/projects/<id>', methods=['GET', 'POST'])
def project(id):
	project = db.projects.find_one({'_id': ObjectId(id)})
	return render_template('project.html', project=project)


@app.route('/login')
def login():
	return render_template('auth/login.html')


@app.route('/register')
def register():
	return render_template('auth/register.html')


@app.route('/logout')
def logout():
	return redirect('/')


@socketio.on('comment', namespace='/comment')
def post_comment(data):
    db.projects.update({'_id': ObjectId(data['id'])}, {'$push': {'comments': data['text']}})
    socketio.emit('comment', data, namespace='/comment')
