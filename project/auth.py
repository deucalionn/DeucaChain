from crypt import methods
from nis import cat
from re import T

from flask import Blueprint, render_template, request, flash
import flask
from flask.helpers import url_for
from flask_login.utils import login_required
from itsdangerous import exc
import requests
from werkzeug.utils import redirect
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash

from .models import User, Article
from . import db
from flask_login import login_user
from .models import User
from uuid import uuid4
import binascii
import os
from werkzeug.utils import secure_filename
import markdown
import markdown.extensions.fenced_code


flask_auth = Blueprint('auth', __name__)


@flask_auth.route('/login')
def login():
    error = 0
    return render_template('login.html', error=error)


@flask_auth.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(name=name).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@flask_auth.route("/uploader", methods=['POST'])
@login_required
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        file_name = f.filename
        title = request.form.get('title')
        category = request.form.get('browsers')
        description = request.form.get('description')

        f.save(os.path.join(
            '/project/static/articles', secure_filename(f.filename)))
        addArticleToDb(title, file_name, category, description)
        flash('Upload succesfully !')
        return redirect(url_for('main.profile'))


def addArticleToDb(title, file_name, category, description):
    print("Adding article")
    article = Article(file_name=file_name, category=category,
                      title=title, description=description)
    db.session.add(article)
    db.session.commit()


@flask_auth.route('/profile/deleteArticle', methods=['POST'])
@login_required
def deleteArticle():
    source = request.form.get('delete')
    article_to_delete = Article.query.filter_by(title=source)
    print(article_to_delete)
    article_to_delete.delete()
    db.session.commit()

    return redirect(url_for('main.profile'))
