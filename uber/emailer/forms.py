from flask_wtf import Form

from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class EmailForm(Form):
    from_email = TextField('From email', validators=[DataRequired(), Email(), Length(max=255)])
    to_email = TextField('To email', validators=[DataRequired(), Email(), Length(max=255)])
    subject = TextField('Subject', validators=[DataRequired(), Length(max=255)])
    body = TextAreaField('Body', validators=[DataRequired(), Length(max=512)])
