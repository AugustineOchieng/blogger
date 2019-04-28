from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import BlogForm,UpdateProfile,CommentForm
from ..import db,photos
from ..models import User,Blog,Comment
from flask_login import login_required,current_user
import markdown2
import requests
@main.route("/")
def index():
  blogs = Blog.query.all()

    title = "Bloggeropolis"
    return render_template("index.html", title = title , blogs = blogs)
