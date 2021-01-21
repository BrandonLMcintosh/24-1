from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired, URL, NumberRange, Optional

class PetForm(FlaskForm):

    name = StringField('Name', validators=[InputRequired()])
    species = SelectField('Species', validators=[InputRequired()], choices=[('cat','cat'),('dog','dog'),('porcupine','porcupine')])
    photo_url = StringField('Photo URL', validators=[Optional(), URL()])
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=0, max=30)])
    notes = TextAreaField('Notes', validators=[Optional()])

    def flash_errors(self):
        for field, errors in self.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(self, field).label.text, error), 'error')