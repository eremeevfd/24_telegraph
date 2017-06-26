from flask import Flask, render_template, request, redirect, url_for, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import cyrtranslit
import datetime
import uuid


basedir = os.path.abspath(os.path.dirname(__file__))
migration_dir = os.path.abspath(os.path.join(basedir, 'migrations'))

app = Flask(__name__)
app.debug = True
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=migration_dir)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(80), index=True)
    signature = db.Column(db.String(80))
    body = db.Column(db.String)
    slug = db.Column(db.String, index=True)
    cookie = db.Column(db.String)

    def __init__(self, header, signature, body, slug, cookie):
        self.header = header
        self.signature = signature
        self.body = body
        self.slug = slug
        self.cookie = cookie

    def __repr__(self):
        return 'Article %r' % self.header


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        header = request.form['header']
        signature = request.form['signature']
        body = request.form['body']
        slug = cyrtranslit.to_latin(request.form['header'], 'ru')
        slug = slug.replace(' ', '-')
        slug = '{slug}-{month}-{day}'.format(slug=slug,
                                             month=datetime.date.today().month,
                                             day=datetime.date.today().day)

        user_id = request.cookies.get('user_id')
        cookie = user_id or str(uuid.uuid4())
        articles_count = db.session.query(Article).filter_by(header=header).count()
        if articles_count != 0:
            slug = "{slug}-{article_counter}".format(slug=slug, article_counter=articles_count + 1)
        new_article = Article(header, signature, body, slug, cookie)
        db.session.add(new_article)
        db.session.commit()

        response = make_response(url_for('article', article_slug=slug))

        if user_id:
            return response
        else:
            response.set_cookie('user_id', cookie, secure=True)
            return response

    return render_template('form.html')


@app.route('/<path:article_slug>', methods=['GET', 'POST'])
def article(article_slug):
    open_article = Article.query.filter_by(slug=article_slug).first()
    cookie = request.cookies.get('user_id')

    if open_article:
        return render_template('article.html', article=open_article, cookie=cookie)
    else:
        abort(404)


@app.route('/<path:article_slug>/edit', methods=['POST'])
def edit_article(article_slug):
    open_article = Article.query.filter_by(slug=article_slug).first()
    header = request.form['header']
    signature = request.form['signature']
    body = request.form['body']
    open_article.header = header
    open_article.signature = signature
    open_article.body = body
    db.session.add(open_article)
    db.session.commit()
    return redirect(url_for('article', article_slug=open_article.slug))


if __name__ == "__main__":
    app.run()
