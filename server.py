from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from translit import transliterate
import datetime


basedir = os.path.abspath(os.path.dirname(__file__) + '/')
migration_dir = os.path.abspath(os.path.join(basedir, 'migrations'))

app = Flask(__name__)
app.debug = True
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=migration_dir)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(80))
    signature = db.Column(db.String(80))
    body = db.Column(db.String)
    url = db.Column(db.String)
    cookie = db.Column(db.String)

    def __init__(self, header, signature, body, url, cookie):
        self.header = header
        self.signature = signature
        self.body = body
        self.url = url
        self.cookie = cookie

    def __repr__(self):
        return 'Article %r' % self.header


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        header = request.form['header']
        signature = request.form['signature']

        body = request.form['body']
        url = transliterate(request.form['header'])
        url = url + '-{month}-{day}'.format(month=datetime.date.today().month,
                                            day=datetime.date.today().day)
        cookie = request.cookies.get('session')
        articles_count = Article.query.filter_by(header=header).count()
        if articles_count != 0:
            url = url + '-{article_counter}'.format(article_counter=articles_count+1)
        new_article = Article(header, signature, body, url, cookie)
        db.session.add(new_article)
        db.session.commit()
        # print(request.cookies.get('session'))
        return redirect(url_for('article', article_url=url))

    return render_template('form.html')


@app.route('/<article_url>', methods=['GET', 'POST'])
def article(article_url):
    open_article = Article.query.filter_by(url=article_url).first()
    cookie = request.cookies.get('session')
    return render_template('article.html', article=open_article, cookie=cookie)


if __name__ == "__main__":
    app.run()
