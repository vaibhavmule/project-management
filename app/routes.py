from flask import render_template, request, redirect
from app import app, mongo, socketio
from bson import ObjectId

@app.route('/')
@app.route('/index')
def index():
	projects = mongo.db.projects.find()
	return render_template('index.html', title='Home', projects=projects)


@app.route('/create', methods=['GET','POST'])
def create_project():
	if request.method == 'POST':
		title = request.form['title']
		mongo.db.projects.insert_one({'title': title})
		return redirect('/')
	return render_template('create.html')


@app.route('/<id>', methods=['GET', 'POST'])
def project(id):
	if request.method == 'POST':
		text = request.form['text']
		mongo.db.projects.update({'_id': ObjectId(id)}, {'$push': {'comments': text}})
		return redirect('/' + id)
	project = mongo.db.projects.find_one({'_id': ObjectId(id)})
	return render_template('project.html', project=project)

@socketio.on('post_comment')
def post_comment(data):
    mongo.db.projects.update({'_id': ObjectId(data['id'])}, {'$push': {'comments': data['text']}})
    socketio.emit('append_comment', data)