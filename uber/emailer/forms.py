from flask_wtf import Form

from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired, Email


class EmailForm(Form):
    from_email = TextField('From email', validators=[DataRequired(), Email()])
    to_email = TextField('To email', validators=[DataRequired(), Email()])
    subject = TextField('Subject', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
