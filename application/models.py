from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
db = SQLAlchemy()

class Roles_Users(db.Model):
    __tablename__ = 'Roles_Users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    role_id = db.Column(db.Integer, db.ForeignKey('Role.id'))

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30) ,nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    roles = db.Relationship('Role',secondary='Roles_Users',backref='Users')
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(), nullable=False)
    fs_uniquifier = db.Column(db.String(255),unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)
    playlists=db.relationship('Playlists',backref='User')


class Role(db.Model, RoleMixin):
    __tablename__ = 'Role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(255))

class User_track(db.Model):
    __tablename__ = 'User_track'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    last_login = db.Column(db.DateTime)

class Albums(db.Model):
    __tablename__ = 'Albums'
    album_id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String(50) ,nullable=False)
    album_art = db.Column(db.String(200), nullable=False)
    album_year = db.Column(db.Integer, nullable=False)
    creator = db.Column(db.Integer,db.ForeignKey('User.user_id'))
    genre = db.Column(db.String(30), nullable=False)
    songs=db.relationship('Songs',backref="Albums",cascade='all,delete')

mtmr=db.Table('mtmr',
              db.Column('pl_id',db.Integer,db.ForeignKey('Playlists.pl_id')),
              db.Column('song_id',db.Integer,db.ForeignKey('Songs.song_id')))

class Playlists(db.Model):
    __tablename__='Playlists'
    pl_id = db.Column(db.Integer, primary_key=True)
    pl_name = db.Column(db.String(50) ,nullable=False)
    pl_year = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('User.user_id'))

class Songs(db.Model):
    __tablename__ = 'Songs'
    song_id = db.Column(db.Integer, primary_key=True)
    album_id= db.Column(db.Integer, db.ForeignKey('Albums.album_id'))
    song_name = db.Column(db.String(30) ,nullable=False)
    song_year = db.Column(db.Integer,nullable=False)
    ratings = db.Column(db.Integer, default=0)
    user_rate_count = db.Column(db.Integer, default=0)
    lyrics = db.Column(db.String(5000),default="No Lyrics Available")
    creator = db.Column(db.Integer,db.ForeignKey('User.user_id'))
    genre=db.Column(db.String(30),nullable=False)
    song_loc = db.Column(db.String(100), nullable=False ,unique=True)
    flagged = db.Column(db.Boolean, default=False, nullable=False)
    plals=db.relationship('Playlists',secondary=mtmr,backref='song_inpl',cascade='save-update, merge, refresh-expire')