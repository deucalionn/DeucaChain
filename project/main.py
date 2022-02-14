from calendar import c
from nis import cat
from os import name
import re
from unicodedata import category
from flask import Blueprint, request, flash, url_for
from flask.templating import render_template
from flask_login import login_required, current_user
from project.auth import login
from flask_login import login_required, current_user
import markdown
import markdown.extensions.fenced_code
from werkzeug.utils import redirect
from flask_mail import Mail, Message
from . import mail

from project.models import User, Article
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    articleInfo = getArticle(category="Informatique")
    articleBlock = getArticle(category="Blockchain")
    articleTuto = getArticle(category="Tutoriel")
    lenInfo = len(articleInfo)
    lenBlock = len(articleBlock)
    lenTuto = len(articleTuto)
    return render_template('interface.html', name=current_user.name, lenInfo=lenInfo, articleInfo=articleInfo, articleBlock=articleBlock, lenBlock=lenBlock, articleTuto=articleTuto, lenTuto=lenTuto)


@main.route('/articles')
def articles():
    articleInfo = getArticle(category="Informatique")
    articleBlock = getArticle(category="Blockchain")
    articleTuto = getArticle(category="Tutoriel")
    lenInfo = len(articleInfo)
    lenBlock = len(articleBlock)
    lenTuto = len(articleTuto)
    return render_template('articles.html', lenInfo=lenInfo, articleInfo=articleInfo, articleBlock=articleBlock, lenBlock=lenBlock, articleTuto=articleTuto, lenTuto=lenTuto)


@main.route("/articles/article")
def printArticles():
    source = request.args.get('name')
    readme_file = open(
        "project/static/articles/"+source, "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )

    return md_template_string


def getArticle(category) -> list:
    print(category)
    if category == "Informatique":
        article = Article.query.filter_by(category="Informatique").all()
    elif category == "Blockchain":
        article = Article.query.filter_by(category="Blockchain").all()
    elif category == "Tutoriel":
        article = Article.query.filter_by(category="Tutoriel").all()
    elif category == "Divers":
        article = Article.query.filter_by(category="Divers").all()

    return article


@main.route('/sendmail', methods=['POST'])
def sendMail():
    if request.method == 'POST':
        name = request.form.get('mail_name')
        email = request.form.get('email')
        message = request.form.get('message_mail')
        msg = Message("Nouveau mail DeucaChain", sender=email,
                      recipients=['myemail'])
        msg.body = "{} send to you : {} email : {}".format(
            name, message, email)
        mail.send(msg)
        flash("Message envoyé ! ")
        return redirect(url_for('main.index',  _anchor='contact'))
