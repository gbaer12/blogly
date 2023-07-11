import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    
    db.app = app
    db.init_app(app)

DEFAULT_IMAGE_URL = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRH-woMrLOEbaHBX9Kwlcbos9pMnd5VDqyckw&usqp=CAU'

class User(db.Model):
    """User"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    first_name = db.Column(db.String(30), 
                           nullable=False, 
                           unique=False)
    last_name = db.Column(db.String(30), 
                          nullable=False, 
                          unique=False)
    image_url = db.Column(db.Text, 
                          nullable=False, 
                          default=DEFAULT_IMAGE_URL)

    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')
    
def __repr__(self):
    u = self
    return f'<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}'


class Post(db.Model):
    """Posts"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    title = db.Column(db.Text, 
                      nullable=False)
    content = db.Column(db.Text, 
                        nullable=False)
    created_at = db.Column(db.DateTime, 
                           nullable=False, 
                           default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'), 
                        nullable=False)
    
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime('%a %b %-d %Y, %-I:%M %p')

class Tag(db.Model):
    """Tags"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)
    
    posts = db.relationship('Post', secondary='posts_tags', cascade='all, delete', backref='tags')
    
class PostTag(db.Model):
    """Tags for Posts"""

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer,
               db.ForeignKey('posts.id'),
               primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)
    
    