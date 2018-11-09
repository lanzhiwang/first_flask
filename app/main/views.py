from datetime import datetime

from flask import Flask
from flask import current_app, g, request, session
# from flask import before_first_request, before_request, after_request, teardown_request
from flask import make_response, render_template
from flask import redirect
from flask import url_for
from flask import abort
from flask import flash

from . import main 
from .forms import NameForm
from ..models import User
from .. import db

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['know'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['know'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())

@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
