from flask import render_template, request, redirect
from app import app, mongo
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


@app.route('/<id>')
def project(id):	
	project = mongo.db.projects.find_one({'_id': ObjectId(id)})
	return render_template('project.html', project=project)
