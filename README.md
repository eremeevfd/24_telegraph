# Telegraph Clone

Clone of Durov's [Telegraph](https://telegra.ph).  
You can visit this example application deployed to heroku [here](https://eremeevfd-telegraph.herokuapp.com/).

# Purpose

This resource is made for fast writing articles. You can do it anonymously or not. Then you get unique link for you article.

# Installation

```
$ pip install -r requirements.txt
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
$ python server.py
```
It runs on [127.0.0.1:5000]( http://127.0.0.1:5000/) by default.

# Features

Application uses SQLite3 by default. If you want to use your own database set environment variable **DATABASE_URL**.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
