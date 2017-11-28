from Golden import app
from flask import render_template 
from Golden import models
from .forms import NewGEOForm
from Golden.eutils import GEODataSet

@app.route('/')
@app.route('/index')
def index():

    studies = models.Study.query.all()
    return render_template('index.html',studies=studies)


@app.route('/add', methods=('GET','POST'))
def add():

    form = NewGEOForm()
    if form.validate_on_submit():
        return render_template('new_geo.html',
                               title='Add {}'.format(form.accession.data),
                               form=form,
                               study=GEODataSet(form.accession.data))

    else:
        return render_template('new_geo.html',
                               title='Add new study',
                               form=form)


