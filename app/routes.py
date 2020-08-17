from flask import render_template
from app import app, mongo

@app.route('/')
@app.route('/index')
def index():
    projects = mongo.db.projects.find()
    return render_template('index.html', title='Home', projects=projects)

@app.route('/create', methods=['GET','POST'])
def create_project():
    # projects = mongo.db.projects
    mongo.db.projects.insert_one({'title': 'Project 1'})
    return render_template('create.html')
