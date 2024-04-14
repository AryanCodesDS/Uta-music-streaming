from flask_restful import Api, Resource, reqparse
from flask import request,send_file,jsonify
import os
from application.models import *
from application.security import datastore
import pandas as pd
import matplotlib.pyplot as plt
from flask_security import auth_required,roles_accepted
from flask_caching import Cache
api = Api()
cache = Cache()

parser = reqparse.RequestParser()
parser.add_argument('song_name', type=str, required=False,help="Song name must be string and is required")
parser.add_argument('new_song_name', type=str, required=False)
parser.add_argument('genre', type=str, required=False,help="Genre must be string and is required")
parser.add_argument('lyrics', type=str, required=False)
parser.add_argument('username', type=str, required=True,help="Creator id must be string and is required")
parser.add_argument('song_id', type=int, required=False,help="Song id must be integer and is required")

class songAPI(Resource):

    @auth_required('token')
    def get(self):
        try:
            songs_obj = Songs.query.all()
            songs = []
            if len(songs_obj) != 0:
                for song in songs_obj:
                    data = {}
                    data['id'] = song.song_id
                    data['Songname'] = song.song_name
                    data['Year'] = song.song_year
                    data['Album'] = Albums.query.filter_by(album_id=song.album_id).first().album_name
                    data['Artist'] = User.query.filter_by(user_id=song.creator).first().name
                    data['Album_art'] = Albums.query.filter_by(album_id=song.album_id).first().album_art
                    data['Genre'] = song.genre  
                    data['Lyrics'] = song.lyrics
                    data['Ratings'] = song.ratings
                    data['Song_location'] = song.song_loc
                    data['flagged'] = song.flagged
                    songs.append(data)
                return jsonify(songs)
            
            else:
                return {'message':'no songs found'},400
        except Exception as e:
            print(e)
            return {'message':'Some error occured'},404

    @auth_required('token')
    @roles_accepted('Creator','Admin')
    def post(self):
        try:
            album_id=request.form.get('albumid')   
            username = str(request.form.get('username'))
            creator = datastore.find_user(username=username).user_id
            upcount = int(request.form.get('upcount'))+1
            print(upcount)
            for i in range(1,upcount):
                song_name=str(request.form.get(f'songs[{i}][name]')).lower().capitalize()
                print(song_name)
                genre=str(request.form.get(f'songs[{i}][genre]')).lower().capitalize()
                lyrics=request.form.get(f'songs[{i}][Lyrics]',type=str)
                file = request.files.get(f'songs[{i}][file]')
                
                UPLOAD_FOLDER = './static/albums/'
                if file.filename == '' or (file.filename.endswith('.mp3')) == False:
                    return {'message': 'No Mp3 file selected '}, 400
                if Songs.query.filter_by(song_name=song_name,creator=creator).first() is not None:
                    return {'message': 'Song already exists'}, 400
                else :
                    album = Albums.query.filter_by(album_id = album_id,creator=creator).first()
                    album_folder = os.path.join(UPLOAD_FOLDER, album.album_name)
                    song_loc = os.path.join(album_folder,file.filename).replace("\\", "/")
                    file.save(song_loc)
                    new_song_loc = os.path.join(album_folder,song_name + '.' + song_loc.split('.')[-1]).replace("\\", "/")
                    os.rename(song_loc,new_song_loc)
                    song = Songs( song_name=song_name, song_year=album.album_year, album_id=album_id, genre=genre, lyrics=lyrics,creator=creator, song_loc=new_song_loc)
                    db.session.add(song)
            db.session.commit()
            cache.clear()
            return {'message': 'Song added successfully'}, 200
        except Exception as e:
            print(e)
            return {'message':'Some error occured'},404

    @auth_required('token')
    @roles_accepted('Creator','Admin')
    def put(self):
        args = parser.parse_args()
        song = Songs.query.filter_by(song_id=args['song_id'],creator = User.query.filter_by(username = args['username']).first().user_id).first()
        if song is None:
            return {'message': 'Song not found'}, 404
        if args['new_song_name'] != None and args['new_song_name'] != '':
            song.song_name = args['new_song_name'].lower().capitalize()
            os.rename(song.song_loc,os.path.join(os.path.dirname(song.song_loc),args['new_song_name'].lower().capitalize() + '.' + song.song_loc.split('.')[-1]).replace("\\", "/"))
            song.song_loc = os.path.join(os.path.dirname(song.song_loc),args['new_song_name'].lower().capitalize() + '.' + song.song_loc.split('.')[-1]).replace("\\", "/")
        if args['genre']  != None and args['genre'] != '' :
            song.genre = args['genre'].lower().capitalize()
        if args['lyrics']  != None and args['lyrics'] != '':
            song.lyrics = args['lyrics']
        db.session.commit()
        cache.clear()
        return {'message': 'Song updated successfully'}, 200

    
    @auth_required('token')
    @roles_accepted('Creator','Admin')
    def delete(self):
        args = parser.parse_args()
        song = Songs.query.filter_by(song_id=args['song_id'],creator = User.query.filter_by(username = args['username']).first().user_id ).first()
        if song is None:
            return {'message': 'Song not found'}, 404
        os.remove(song.song_loc)
        db.session.delete(song)
        db.session.commit()
        cache.clear()
        return {'message': 'Song deleted successfully'}, 200

albumparser = reqparse.RequestParser()
albumparser.add_argument('album_name', type=str, required=False)
albumparser.add_argument('album_id', type=int, required=False)
albumparser.add_argument('new_album_name', type=str, required=False)
albumparser.add_argument('albumgenre', type=str, required=False)
albumparser.add_argument('albumyear', type=str, required=False)
albumparser.add_argument('username', type=str, required=True,help="Creator id must be string and is required")

class albumAPI(Resource):
    @auth_required('token')
    @cache.cached(timeout=300,key_prefix='albums')
    def get(self):
        opt = request.args.get('alt', default = True, type = bool)
        uid = request.args.get('username', default = None, type = str)
        if uid != None:
            albums_obj = Albums.query.filter_by(creator=User.query.filter_by(username=uid).first().user_id).all()
        else:
            albums_obj = Albums.query.all()
        albums = []
        i=1
        if opt == True:
            for album in albums_obj:
                data = {}
                data['id'] = album.album_id
                data['name'] = album.album_name
                data['year'] = album.album_year
                data['genre'] = album.genre
                data['artist'] = User.query.filter_by(user_id = album.creator).first().name
                data['Songs'] = []
                for song in album.songs:
                    data['Songs'].append({
                        'id':song.song_id,
                        'Name': song.song_name,
                        'Year' : song.song_year,
                        'Genre' : song.genre,
                        'Lyrics' : song.lyrics,
                        'Ratings' : song.ratings,
                        'Song_Location' : song.song_loc,
                        'flagged' : song.flagged
                    })
                albums.append(data) 
        else:
            for album in albums_obj:
                data = {}
                data['id'] = album.album_id
                data['name'] = album.album_name
                data['year'] = album.album_year
                data['genre'] = album.genre
                data['artist'] = User.query.filter_by(user_id = album.creator).first().name
                albums.append(data)
        return jsonify(albums)
    
    @roles_accepted("Creator","Admin")
    def post(self):
        try :
            album_name=request.form.get('album_name').lower().capitalize().strip()
            album_year=request.form.get('album_year')
            creator = request.form.get('username')
            upcount = int(request.form.get('upcount'))+1
            artist = datastore.find_user(username = creator)
            genre=request.form.get('genre').lower().capitalize()
            file = request.files.get('album_art')
            UPLOAD_FOLDER = './static/albums'
            if file.filename == '' or (file.filename.endswith('.jpg')) == False:
                return {'message': 'No Image file selected '}, 400
            if Albums.query.filter_by(album_name=album_name,creator=artist.user_id).first() is not None:
                return {'message': 'Album already exists'}, 400
            else :
                album_folder = os.path.join(UPLOAD_FOLDER, album_name)
                print(album_folder)
                print(os.path.exists(album_folder))
                if not os.path.exists(album_folder):
                    os.makedirs(album_folder,exist_ok=True)
                album_art = os.path.join(album_folder,'album_art.' + file.filename.rsplit('.', 1)[1].lower()).replace("\\", "/")
                file.save(album_art)
                album = Albums( album_name=album_name, album_year=album_year, creator=artist.user_id, genre=genre, album_art=album_art)
                db.session.add(album)
                db.session.commit()
                for i in range(1,upcount):
                    song_name=str(request.form.get(f'songs[{i}][name]')).lower().capitalize()
                    genre=str(request.form.get(f'songs[{i}][genre]')).lower().capitalize()
                    lyrics=request.form.get(f'songs[{i}][Lyrics]',type=str)
                    file = request.files.get(f'songs[{i}][file]')
                    UPLOAD_FOLDER = './static/albums/'
                    if file.filename == '' or (file.filename.endswith('.mp3')) == False:
                        return {'message': 'No Mp3 file selected '}, 400
                    if Songs.query.filter_by(song_name=song_name,creator=creator).first() is not None:
                        return {'message': 'Song already exists'}, 400
                    else :
                        album_folder = os.path.join(UPLOAD_FOLDER, album_name)
                        song_loc = os.path.join(album_folder,file.filename).replace("\\", "/")
                        file.save(song_loc)
                        new_song_loc = os.path.join(album_folder,song_name + '.' + song_loc.split('.')[-1]).replace("\\", "/")
                        os.rename(song_loc,new_song_loc)
                        song = Songs( song_name=song_name, song_year=album.album_year, album_id=album.album_id, genre=genre, lyrics=lyrics,creator=artist.user_id, song_loc=new_song_loc)
                        db.session.add(song)
                db.session.commit()
                cache.clear()
                return {'message': 'Album added successfully'}, 200
        except  Exception as e:
            print(e)
            return {'message': 'No Album added'}, 400
    
    @auth_required('token')
    @roles_accepted('Creator','Admin')
    def put(self):
        args = albumparser.parse_args()
        creator=datastore.find_user(username=args['username'])
        album = Albums.query.filter_by(album_id=args['album_id'],creator=creator.user_id).first()
        if album is None:
            return {'message': 'Album not found'}, 404
        if args['new_album_name'] != None and args['new_album_name'] != '':
            album_name = args['new_album_name'].lower().capitalize()
            curr_folder = f'./static/albums/{album.album_name}'
            new_folder = f'./static/albums/{album_name}'
            os.rename(curr_folder,new_folder)
            if album.songs:
                for song in album.songs:
                    song.album_name = album_name
                    song.song_loc = os.path.join(new_folder,song.song_loc.split('/')[-1]).replace("\\", "/")
            album.album_art = os.path.join(new_folder,album.album_art.split('/')[-1]).replace("\\", "/")
            album.album_name = album_name
        if args['albumgenre']  != None and args['albumgenre'] != '':
            album.genre = args['albumgenre'].lower().capitalize()
        if args['albumyear']  != None and args['albumyear'] != '':
            album.album_year = args['albumyear']
            if album.songs:
                for song in album.songs:
                    song.song_year = args['albumyear']

        db.session.commit()
        cache.clear()
        return {'message': 'Album updated successfully'}, 200
    
    @auth_required('token')
    @roles_accepted('Creator','Admin')
    def delete(self):
        args = albumparser.parse_args()
        creator=datastore.find_user(username=args['username'])
        album_todel = Albums.query.filter_by(album_id=args['album_id'],creator=creator.user_id).first()
        album_folder = f'./static/albums/{album_todel.album_name}'
        songs_del = Songs.query.filter_by(album_id=album_todel.album_id).all()
        if songs_del:
            for song in songs_del:
                db.session.delete(song)
        import shutil
        shutil.rmtree(album_folder)
        db.session.delete(album_todel)
        db.session.commit()
        cache.clear()
        return {'message': 'Album deleted successfully'}, 200

api.add_resource(songAPI, '/api/songs','/api/songs/add','/api/songs/update','/api/songs/delete')
api.add_resource(albumAPI, '/api/albums','/api/albums/add','/api/albums/update','/api/albums/delete')