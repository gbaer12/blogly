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
    
def __repr__(self):
    u = self
    return f'<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}'


