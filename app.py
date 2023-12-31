from flask import Flask, request, render_template, redirect, session, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
def show_homepage():
    """Show Blogly Homepage"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template('home.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page"""

    return render_template('404.html'), 404

@app.route('/users')
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
    tags = Tag.query.all()

    return render_template('create_post.html', user=user, tags=tags)

@app.route('/<int:user_id>', methods=['POST'])
def create_post(user_id):
    """Generate post from post form."""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_title = request.form['title']
    new_content = request.form['content']
    new_post = Post(title=new_title,
                    content=new_content,
                    user_id=user_id,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/{user_id}')

@app.route('/<int:user_id>/<int:post_id>')
def show_post(user_id, post_id):
    """Show post from user."""

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('post_detail.html', user=user, post=post, tags=tags)

@app.route('/<int:user_id>/<int:post_id>/edit')
def show_post_edit(user_id, post_id):
    """Show form to edit the Post."""
    
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    
    return render_template('edit_post.html', user=user, post=post, tags=tags)    

@app.route('/<int:user_id>/<int:post_id>/edit', methods=['POST'])
def edit_post(user_id, post_id):
    """Generate edited post from form."""

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

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

@app.route('/tag/list')
def show_tag_list():
    """Shows the tag list page."""

    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags)

@app.route('/create/tag')
def create_tag_form():
    """Show form to create a Tag."""

    return render_template('create_tag.html')

@app.route('/tag/list', methods=['POST'])
def create_tag():
    """Generate new tag from form."""

    tag = request.form['name']
    new_tag = Tag(name=tag)

    db.session.add(new_tag)
    db.session.commit()

    return redirect(f'/tag/list')

@app.route('/tag/<int:tag_id>')
def tag_edit_form(tag_id):
    """Show the Tag Edit form."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit_tag.html', tag=tag)

@app.route('/tag/<int:tag_id>', methods=['POST'])
def tag_edit(tag_id):
    """Show the Tag Edit form."""

    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()

    return redirect('/tag/list')

@app.route('/tag/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete tag"""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tag/list')

