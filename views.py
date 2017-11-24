from Golden import app
from flask import render_template 

@app.route('/')
@app.route('/index')
def index():

    studies = [
        {
            'name' : 'Abad_2013',
            'date' : 'Feb 12 2013',
            'title': 'Reprogramming in vivo produces teratomas and iPS cells with totipotency features.'
        },
        {
            'name' : 'Adachi_2013',
            'date' : 'Mar 14 2013',
            'title': 'Context-Dependent Wiring of Sox2 Regulatory Networks for Self-Renewal of Embryonic and Trophoblast Stem Cells.'
        },
        {
            'name' : 'Aloia_2014',
            'date' : 'July 23 2014',
            'title': 'Zrf1 is required to establish and maintain neural progenitor identity.'
        },

    ]

    return render_template('index.html',studies=studies)
