from flask import Flask, render_template, redirect, url_for
from .form import regf, login1
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

app.app_context().push()


class user1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zviaz = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.Integer)
    live = db.Column(db.String)
    prof = db.Column(db.String)
    age = db.Column(db.Integer, nullable=False)



class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=False)
    email = db.Column(db.String, nullable=True, unique=True)

@app.route('/')
def main():
    users=user.query.all()
    return render_template('home.html', users=users)


@app.route('/st1')
def main1():
    name1='ded1'
    return render_template('st1.html', b=name1)


@app.route('/st2')
def main2():
    name2='ded2'
    return render_template('st2.html', a=name2)

@app.route('/st3')
def main3():
    name2='ded3'
    return render_template('st3.html', c=name2)


@app.route('/reg', methods=["POST", 'GET'])
def reg():
    form = regf()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        u = user(username=username, email=email, password=password)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('reg.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = login1()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = user1.query.filter_by(username=username).first()
        if user is None or password != user.password:
            return redirect('/login')
        login_user(user, remember=form.remember.data)
        return redirect(url_for('main'))
    return render_template('login.html', form=form, title=login1)

@login.user_loader
def load_user(id):
    return user.