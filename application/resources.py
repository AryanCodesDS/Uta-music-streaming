from flask_restful import Api, Resource, reqparse
from flask import request,send_file
import os
from application.models import *
import pandas as pd
import matplotlib.pyplot as plt
from flask_security import auth_required,roles_required,login_required
api = Api()

parser = reqparse.RequestParser()
parser.add_argument('song_name', type=str, required=True,help="Song name must be string and is required")
parser.add_argument('new_song_name', type=str, required=False)
parser.add_argument('genre', type=str, required=True,help="Genre must be string and is required")
parser.add_argument('lyrics', type=str, required=False)
parser.add_argument('creator_id', type=int, required=True,help="Creator id must be integer and is required")

class songAPI(Resource):
    @auth_required('token')
    def get(self):
        songs_obj = Songs.query.all()
        songs = {}
        i=1
        for song in songs_obj:
            data = {}
            data['Song name'] = song.song_name
            data['Year'] = song.song_year
            data['Album name'] = Albums.query.filter_by(album_id=song.album_id).first()
            data['Genre'] = song.genre  
            data['Lyrics'] = song.lyrics
            data['Ratings'] = song.ratings
            songs[f'song_{i}'] = data
            i += 1
        return songs
    
    @roles_required('Creator','Admin')
    @auth_required('token')
    def post(self):
        song_name=request.form.get('song_name').lower().capitalize()
        song_year=request.form.get('song_year')
        album_name=request.form.get('album_name').lower().capitalize()
        creator = request.form.get('creator_id')
        genre=request.form.get('genre').lower().capitalize()
        lyrics=request.form.get('lyrics')
        file = request.files.get('song_file')
        UPLOAD_FOLDER = './static/albums/'
        if file.filename == '' or (file.filename.endswith('.mp3')) == False:
            return {'message': 'No Mp3 file selected '}, 400
        if Songs.query.filter_by(song_name=song_name,creator=creator).first() is not None:
            return {'message': 'Song already exists'}, 400
        if Albums.query.filter_by(album_name=album_name).first() is None:
            return {'message': 'Album not found'}, 404
        else :
            album = Albums.query.filter_by(album_name=album_name,creator=creator).first()
            album_id = album.album_id
            album_folder = os.path.join(UPLOAD_FOLDER, album.album_name)
            song_loc = os.path.join(album_folder,file.filename).replace("\\", "/")
            file.save(song_loc)
        song = Songs( song_name=song_name, song_year=song_year, album_id=album_id, genre=genre, lyrics=lyrics,creator=creator, song_loc=song_loc)
        db.session.add(song)
        db.session.commit()
        return {'message': 'Song added successfully'}, 201

    @roles_required('Creator','Admin')
    @auth_required('token')
    def put(self):
        args = parser.parse_args()
        song = Songs.query.filter_by(song_name=args['song_name'].lower().capitalize(),creator = args['creator_id'] ).first()
        if song is None:
            return {'message': 'Song not found'}, 404
        if args['new_song_name'] != None:
            song.song_name = args['new_song_name'].lower().capitalize()
        if args['genre']  != None :
            song.genre = args['genre'].lower().capitalize()
        if args['lyrics']  != None :
            song.lyrics = args['lyrics']
        db.session.commit()
        return {'message': 'Song updated successfully'}, 200

    @roles_required('Creator','Admin')
    @auth_required('token')
    def delete(self):
        args = parser.parse_args()
        song = Songs.query.filter_by(song_name=args['song_name'],creator = args['creator_id'] ).first()
        if song is None:
            return {'message': 'Song not found'}, 404
        os.remove(song.song_loc)
        db.session.delete(song)
        db.session.commit()
        return {'message': 'Song deleted successfully'}, 200

albumparser = reqparse.RequestParser()
albumparser.add_argument('album_name', type=str, required=True)
albumparser.add_argument('new_album_name', type=str, required=False)
albumparser.add_argument('albumgenre', type=str, required=False)
albumparser.add_argument('albumyear', type=str, required=False)
albumparser.add_argument('creator_id', type=int, required=True)

class albumAPI(Resource):
    @auth_required('token')
    def get(self):
        opt = request.args.get('alt', default = True, type = bool)
        albums_obj = Albums.query.all()
        albums = {}
        i=1
        if opt == True:
            for album in albums_obj:
                data = {}
                data['Album name'] = album.album_name
                data['Album year'] = album.album_year
                data['Album genre'] = album.genre
                data['Album artist'] = User.query.filter_by(user_id = album.creator).first().name
                data['Songs'] = []
                for song in album.songs:
                    data['Songs'].append({
                        'Song name': song.song_name,
                        'Year' : song.song_year,
                        'Genre' : song.genre,
                        'Lyrics' : song.lyrics,
                        'Ratings' : song.ratings
                    })
                albums[f'album_{i}'] = data
                i += 1
        else:
            for album in albums_obj:
                data = {}
                data['Album name'] = album.album_name
                data['Album year'] = album.album_year
                data['Album genre'] = album.genre
                data['Album artist'] = User.query.filter_by(user_id = album.creator).first().name
                albums[f'album_{i}'] = data
                i += 1
        return albums
    
    @roles_required('Creator','Admin')
    @auth_required('token')
    def post(self):
        album_name=request.form.get('album_name').lower().capitalize()
        album_year=request.form.get('album_year')
        creator = request.form.get('creator_id')
        artist = User.query.filter_by(user_id=creator).first().name
        genre=request.form.get('genre').lower().capitalize()
        file = request.files.get('album_art')
        UPLOAD_FOLDER = './static/albums/'
        if file.filename == '' or (file.filename.endswith('.jpg') or file.filename.endswith('.png')) == False:
            return {'message': 'No Image file selected '}, 400
        if Albums.query.filter_by(album_name=album_name,creator=creator).first() is not None:
            return {'message': 'Album already exists'}, 400
        else :
            album_folder = os.path.join(UPLOAD_FOLDER, album_name)
            if not os.path.exists(album_folder):
                os.mkdir(album_folder)
            album_art = os.path.join(album_folder,'album_art.' + file.filename.rsplit('.', 1)[1].lower()).replace("\\", "/")
            file.save(album_art)
        album = Albums( album_name=album_name, album_year=album_year, creator=creator,creator_name = artist , genre=genre, album_art=album_art)
        db.session.add(album)
        db.session.commit()
        return {'message': 'Album added successfully'}, 201
    
    @roles_required('Creator','Admin')
    @auth_required('token')
    def put(self):
        args = albumparser.parse_args()
        album = Albums.query.filter_by(album_name=args['album_name'].lower().capitalize(),creator = args['creator_id'] ).first()
        if album is None:
            return {'message': 'Album not found'}, 404
        if args['new_album_name'] != None:
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
        if args['albumgenre']  != None :
            album.genre = args['albumgenre'].lower().capitalize()
        if args['albumyear']  != None :
            album.album_year = args['albumyear']
        db.session.commit()
        return {'message': 'Album updated successfully'}, 200
    
    @roles_required('Creator','Admin')
    @auth_required('token')
    def delete(self):
        args = albumparser.parse_args()
        album_todel = Albums.query.filter_by(album_name=args['album_name'].lower().capitalize(),creator =  args['creator_id']).first()
        album_folder = f'static/albums/{album_todel.album_name}'
        songs_del = Songs.query.filter_by(album_id=album_todel.album_id,album_name=album_todel.album_name).all()
        if songs_del:
            for song in songs_del:
                db.session.delete(song)
        import shutil
        shutil.rmtree(album_folder)
        db.session.delete(album_todel)
        db.session.commit()
        return {'message': 'Album deleted successfully'}, 200

graphparser = reqparse.RequestParser()
graphparser.add_argument('admin_id', type=int, required=True)
graphparser.add_argument('graph_type', type=str, required=True)

class GraphAPI(Resource):
    def get(self):
        file_path = './static/admin/plot.png'
        return send_file(file_path, mimetype='image/png')

    def post(self):
        args = graphparser.parse_args()
        admin = User.query.filter_by(user_id=args['admin_id']).first()
        if admin is None:
            return {'message': 'Admin not found'}, 404
        if args['graph_type'] == 'pie':
            genre_pie = Songs.query.with_entities(Songs.genre).all()
            genre_df = pd.DataFrame(genre_pie, columns=['Genre'])
            plt.switch_backend('agg')
            plt.figure(figsize=(8, 4))
            plt.pie(genre_df['Genre'].value_counts(), labels=genre_df['Genre'].unique(), autopct='%1.1f%%',textprops={'fontsize': 12})
            plt.title('Genre Distribution')
            plt.savefig(os.path.join('./static/admin/', 'plot.png'))
            plt.close()
        elif args['graph_type'] == 'bar':
            album_years = Albums.query.with_entities(Albums.album_year).all()
            album_years_df = pd.DataFrame(album_years, columns=['Year'])
            df_temp = album_years_df['Year'].value_counts()
            df_final = df_temp.reset_index()
            df_final.columns = ['Year', 'Uploads']
            df_final = df_final.sort_values(by=['Year'], ascending=True)
            plt.switch_backend('agg')
            plt.figure(figsize=(8, 4))
            plt.title('Album Uploads in last 5 Years')
            plt.xlabel('Year')
            plt.ylabel('Uploads')
            plt.bar(df_final['Year'], df_final['Uploads'])
            plt.xticks(df_final['Year'])
            plt.yticks(range(0, int(max(df_final['Uploads'])) + 1))
            plt.savefig(os.path.join('./static/admin/', 'plot.png'))
            plt.close()
        return {'message': 'Graph generated successfully for admin f{admin.name}'}, 200

api.add_resource(songAPI, '/api/songs','/api/songs/add','/api/songs/update','/api/songs/delete')
api.add_resource(albumAPI, '/api/albums','/api/albums/add','/api/albums/update','/api/albums/delete')
api.add_resource(GraphAPI, '/api/graph','/api/graph/generate')