from flask import flash
from flask import render_template

from models import *

from uber import emailer
from uber.emailer import app
from uber.emailer.forms import EmailForm


@app.route('/', methods=['GET', 'POST'])
def index():
    form = EmailForm()

    if form.validate_on_submit():
        from_email = form.from_email.data
        to_email = form.to_email.data
        subject = form.subject.data
        body = form.body.data

        success = emailer.send(from_email, to_email, subject, body)

        if success:
            flash('Email sent!', 'success')
        else:
            flash('There was a problem sending your email! Please try again later.', 'error')

    recent_results = EmailServiceResult.objects.order_by('-timestamp').limit(20)

    return render_template('index.html', form=form, recent_results=recent_results)