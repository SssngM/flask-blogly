"""Blogly application."""

from flask import Flask,request, redirect, render_template,  url_for
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)



@app.route("/")
def list_users():
    """user list."""

    users = User.query.all()
    return render_template("index.html", users=users)

@app.route("/new")
def add_form():
    """show from"""
    return render_template("addForm.html")


@app.route("/new", methods=["POST"])
def add_user():
    """edit users"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    # return redirect(f"/{new_user.id}")
    return redirect("/")

@app.route("/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html",user=user)
    #detail.html


@app.route("/<int:user_id>/edit")
def edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("editForm.html", user=user)


@app.route("/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """add users"""
    
    edit_user = User.query.get_or_404(user_id)
    edit_user.first_name = request.form['first_name']
    edit_user.last_name = request.form['last_name']
    edit_user.image_url = request.form['image_url']
    #breakpoint()
    db.session.add(edit_user)
    db.session.commit()

    # return redirect(f"/{new_user.id}")
    return redirect("/")

@app.route("/<int:user_id>/delete")
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    uesrs = User.query.all()
    # return render_template("index.html")
    return redirect("/")