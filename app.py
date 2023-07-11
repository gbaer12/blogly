from flask import Flask, request, render_template, redirect, session, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_user_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretysecret1234'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def list_users():
    """Show list of all Blogly users"""

    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/create')
def get_create():
    """Generate the create user form."""

    return render_template('create.html')

@app.route('/', methods=['POST'])
def create_user():
    """Form that creates a new Blogly user"""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/{new_user.id}')

@app.route('/<int:user_id>')
def show_user(user_id):
    """Show details about the Blogly user"""

    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/<int:user_id>/edit')
def show_edit(user_id):
    """Generate edit user form"""
   
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Form that edits a Blogly user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['image-url']

    db.session.add(user)
    db.session.commit()

    return render_template('details.html', user=user)

@app.route('/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Permanently delete user from Blogly"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/')

@app.route('/<int:user_id>/posts')
def show_post_form(user_id):
    """Show form to create a user post."""

    user = User.query.get_or_404(user_id)
    return render_template('create_post.html', user=user)

@app.route('/<int:user_id>', methods=['POST'])
def create_post(user_id):
    """Generate post from post form."""

    user = User.query.get_or_404(user_id)

    new_title = request.form['title']
    new_content = request.form['content']
    new_post = Post(title=new_title,
                    content=new_content,
                    user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/{user_id}')

@app.route('/<int:user_id>/<int:post_id>')
def show_post(user_id, post_id):
    """Show post from user."""

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', user=user, post=post)

@app.route('/<int:user_id>/<int:post_id>/edit')
def show_post_edit(user_id, post_id):
    """Show form to edit the Post."""
    
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    
    return render_template('edit_post.html', user=user, post=post)    

@app.route('/<int:user_id>/<int:post_id>/edit', methods=['POST'])
def edit_post(user_id, post_id):
    """Generate edited post from form."""

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/{user.id}/{post.id}')

@app.route('/<int:user_id>/<int:post_id>/delete', methods=['POST'])
def delete_post(user_id, post_id):
    """Delete post."""

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/{user.id}')