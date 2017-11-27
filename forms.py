from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class NewGEOForm(FlaskForm):
    accession = StringField('accession', validators=[DataRequired()])

