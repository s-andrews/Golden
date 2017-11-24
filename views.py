from Golden import app
from flask import render_template 
from Golden import models

@app.route('/')
@app.route('/index')
def index():

    studies = models.Study.query.all()

    return render_template('index.html',studies=studies)
