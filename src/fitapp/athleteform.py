'''
    GD 20210227

    The form to allow CRUD of an Athlete
'''

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired


class AthleteForm( FlaskForm ):
    ''' The Athlete form '''

    # Class properties apparently, not instance
    name = StringField( "Name", validators=[DataRequired()] )
    age = IntegerField( "Age", validators=[DataRequired()] )
    weight = DecimalField( "Weight", places=1, validators=[DataRequired()] )
    comment = StringField( "Comment" )
    startdate = DateField( "StartDate" )
    enddate = DateField( "EndDate" )
    