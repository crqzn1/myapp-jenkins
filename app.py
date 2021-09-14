import os
import config

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'xxx'
app.config.from_object(config)

db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    def __repr__(self):
        return "<Title: {}>".format(self.title)

class Author(db.Model):
    __tablename__ = 'authors'
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    book_title = db.Column(db.String(80), db.ForeignKey('books.title'))
    def __repr__(self):
        return "<Author: {}>".format(self.name)

db.drop_all()
db.create_all()

book1 = Book(title="San Guo")
book2 = Book(title="Shui Hu")
db.session.add_all([book1, book2])
db.session.commit()
author1 = Author(name="Wu", book_title=book1.title)
author2 = Author(name="Shi", book_title=book2.title)
db.session.add_all([author1, author2])
db.session.commit()


@app.route("/", methods=["GET","POST"])
def home():
    if request.form:
        try:
            book = Book(title=request.form.get("title"))
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    books = Book.query.all()
    return render_template("home.html", books=books)


@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    book = Book.query.filter_by(title=oldtitle).first()
    book.title = newtitle
    db.session.commit()
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000, debug=True)
