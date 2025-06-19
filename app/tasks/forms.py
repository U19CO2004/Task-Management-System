from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import DateTimeLocalField  # ✅ New, WTForms 3.x+


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    assigned_to = SelectField('Assign to', coerce=int, validators=[DataRequired()])
    deadline = DateTimeLocalField('Deadline', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('Pending', 'Pending'), 
        ('In Progress', 'In Progress'), 
        ('Completed', 'Completed')
    ])
    submit = SubmitField('Save Task')
