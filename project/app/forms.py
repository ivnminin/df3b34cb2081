from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class TaskForm(FlaskForm):

    function = StringField("Function", validators=[DataRequired()])
    interval = StringField("Interval", validators=[DataRequired()])
    step = StringField("Step", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_function(self, function):
        if not isinstance(function.data, str):
            raise ValidationError('Need string')

    def validate_interval(self, interval):
        if not interval.data.isdigit():
            raise ValidationError('Need int')

    def validate_step(self, step):
        if not step.data.isdigit():
            raise ValidationError('Need int')
