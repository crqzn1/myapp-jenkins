import os

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)

app.config.from_object(config)

# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://xxx:yyy@localhost:3306/zzz"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_COMMIT_TEARDOWN"] = True
# app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.secret_key = 'xxx'

db = SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    def __repr__(self):
        return "<Title: {}>".format(self.title)

# @app.route("/")
# def home():
    # return "My flask app"
    # return render_template("home.html")

# @app.route("/", methods=["GET","POST"])
# def home():
#     if request.form:
#         print(request.form)
#     return render_template("home.html")

db.drop_all()
db.create_all()

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
