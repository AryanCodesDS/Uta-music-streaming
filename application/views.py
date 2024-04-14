from flask import current_app as app,request,jsonify,make_response,send_from_directory,url_for
from application.models import db,User_track
from werkzeug.security import check_password_hash as check_hash
from werkzeug.security import generate_password_hash as hash
from application.security import datastore
from flask_security import roles_accepted,auth_required
from application.models import Songs,Albums,Playlists,User
from datetime import datetime,date
from application.resources import cache
current_year = datetime.now().year
current_day = date.today()


@app.post('/user-signup')
def usignup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    name = data.get('name')
    if datastore.find_user(email=email):
        return jsonify({"error": "User already exists"}),400
    user = datastore.create_user(email=email,password=hash(password),roles=["General"],username=username,name=name,active=True)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User Created"}),201

@cache.cached(timeout=100)
@app.post('/user-login')
def ulogin():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if username == None :
        user = datastore.find_user(email = email)
    elif email == None:
        user = datastore.find_user(username = username)
    if user :
        if check_hash(user.password,password):
            rec = User_track.query.filter_by(user_id= user.user_id).first()
            if rec == None:
                track = User_track(user_id = user.user_id,last_login=current_day)
                db.session.add(track)
                db.session.commit()
            else:
                rec.last_login = current_day
                db.session.commit()

            userroles = [u.name for u in user.roles]
            response = make_response(jsonify({"authtoken": user.get_auth_token(),"uname":user.username,"roles":userroles}), 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            print(user.roles)
            return response,200
        else:
            return jsonify({"error": "Invalid Password"}),400
    else:
        return jsonify({"error": "User Not Found"}),400

@app.post('/admin-login')
def adlogin():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user  = datastore.find_user(email = email)
    if user and "Admin" in user.roles:
        if check_hash(user.password,password):
            userroles = [u.name for u in user.roles]
            response = make_response(jsonify({"authtoken": user.get_auth_token(),"username": user.username,"roles": userroles}), 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            return jsonify({"error": "Invalid Password"}),400
    else:
        return jsonify({"error": " Not An Admin"}),400

@app.post('/signup-creator')
def signc():
    data = request.json
    user  = datastore.find_user(username = data.get('username'))
    cache.clear()
    if datastore.add_role_to_user(user,"Creator") == False:
        response = make_response(jsonify({"NotSucess":"You are creator already"}), 400)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        response = make_response(jsonify({"Sucess":"You are creator now"}), 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        datastore.add_role_to_user(user,"Creator")
        db.session.commit()
        return response

@cache.cached(timeout=300)
@app.route('/api/album-art/<path:filename>')
def album_art(filename):
    return send_from_directory('./static', 'albums/'+filename)

@cache.cached(timeout=300)
@app.route('/api/song/<path:filename>')
def album_song(filename):
    return send_from_directory('./static', 'albums/'+filename)


@app.route("/api/rate/<string:song>/<int:rate>",methods=["GET","POST"])
def rate(rate,song):
    curr_song=Songs.query.filter_by(song_name = song).first()
    temp_rating = rate
    curr_song.ratings = round((curr_song.ratings * curr_song.user_rate_count + temp_rating) / (curr_song.user_rate_count + 1),1)
    curr_song.user_rate_count += 1
    db.session.commit()
    cache.clear()
    return jsonify({"rating":curr_song.ratings}),200

@cache.cached(timeout=300)
@app.get('/profile/<username>')
def profile(username):
    user = datastore.find_user(username = username)
    songs = Songs.query.filter_by(creator = user.user_id).all()
    albums = Albums.query.filter_by(creator = user.user_id).all()
    counts = [len(songs),len(albums)]
    user_rates = 0
    for u in songs:
        user_rates += u.user_rate_count
    
    response = {
        "Name" : user.name,
        "Totalsongs": counts[0],
        "Totalalbums" : counts[1],
        "userrates" : user_rates
    }
    return jsonify(response),200


@cache.cached(timeout=100)
@app.get('/api/playlist/<username>')
def playlist(username):
    user = datastore.find_user(username = username)
    playlist = Playlists.query.filter_by(uid=user.user_id).all()
    pls = []
    for p in playlist:
        pl = {
            "id": p.pl_id,
            "name": p.pl_name,
            "year": p.pl_year
        }
        songs = p.song_inpl
        songlist = []
        for song in songs:
            songlist.append({
                "name": song.song_name,
                "year": song.song_year,
                "genre": song.genre,
                "album": Albums.query.filter_by(album_id = song.album_id).first().album_name,
                "ratings": song.ratings,
                "creator": datastore.find_user(user_id = song.creator).name,
                })
        pl["songs"] = songlist
        pls.append(pl)
    return jsonify(pls),200


@cache.cached(timeout=100)
@app.get('/api/playlist/<username>/<int:pid>')
def playlist_curr(username,pid):
    user = datastore.find_user(username = username)
    p = Playlists.query.filter_by(uid=user.user_id,pl_id=pid).first()
    pl = {
        "name": p.pl_name,
        "year": p.pl_year,
        "creator": user.name,
    }
    songs = p.song_inpl
    songlist = []
    for song in songs:
        songlist.append({
            "name": song.song_name,
            "year": song.song_year,
            "genre": song.genre,
            "album": Albums.query.filter_by(album_id = song.album_id).first().album_name,
            "ratings": song.ratings,
            "creator": datastore.find_user(user_id = song.creator).name,
            })
    pl["songs"] = songlist
    return jsonify(pl),200



@app.post('/api/playlist/<name>/<username>/<int:songid>')
def addpl(name,username,songid):
    user = datastore.find_user(username = username)
    ple = Playlists.query.filter_by(pl_name = name).first()
    cache.clear()
    if ple:
        song = Songs.query.filter_by(song_id = songid).first()
        if song in ple.song_inpl:
            return jsonify({"error":"Song Already Exists in Playlist"}),400
        ple.song_inpl.append(song)
        db.session.commit()
        return jsonify({"error":"Song Added to Playlist"}),200
    else:
        pl = Playlists(pl_name = name,uid=user.user_id,pl_year=current_year)
        db.session.add(pl)
        song = Songs.query.filter_by(song_id = songid).first()
        pl.song_inpl.append(song)
        db.session.commit()
        return jsonify({"message":"Playlist Created"}),200
    

@cache.cached(timeout=300)
@app.get('/customapi/album/<int:id>')
def album(id):
    album = Albums.query.filter_by(album_id = id).first()
    songs = Songs.query.filter_by(album_id = id).all()
    artist = datastore.find_user(user_id = album.creator)
    songlist = []
    for song in songs:
        songlist.append({
            "name": song.song_name,
            "year": song.song_year,
            "genre": song.genre,
            "ratings": song.ratings,
            "creator": song.creator,
            "lyrics": song.lyrics,
            })
    response = {
        "name": album.album_name,
        "year": album.album_year,
        "genre": album.genre,
        "creator": artist.name,
        "songs": songlist
    }
    return jsonify(response),200

@cache.cached(timeout=300)
@app.get('/api/profile/<username>')
def uprofile(username):
    user = datastore.find_user(username = username)
    response = {
        "Name" : user.name,
        "email" : user.email,
    }
    return jsonify(response),200

@cache.cached(timeout=30)
@roles_accepted('Admin')
@auth_required('token')
@app.get('/app/stats')
def stats():
    users = User.query.all()
    creator_count = [u for u in users if "Creator" in [r.name for r in u.roles]]
    general_count = [u for u in users if "General" in [r.name for r in u.roles]]
    songs = Songs.query.all()
    albums = Albums.query.all()
    song_genre_count= {}
    for song in songs:
        if song.genre in song_genre_count:
            song_genre_count[song.genre] += 1
        else:
            song_genre_count[song.genre] = 1

    response = {
        "users": len(users),
        "songs": len(songs),
        "albums": len(albums),
        "creators": len(creator_count),
        "generals": len(general_count),
        "song_genre_count": song_genre_count
    }
    return jsonify(response),200


@roles_accepted('Admin')
@auth_required('token')
@app.delete('/admin/songs/delete/<int:id>')
def delete_song(id):
    song = Songs.query.filter_by(song_id = id).first()
    db.session.delete(song)
    db.session.commit()
    cache.clear()
    return jsonify({"message":"Song Deleted"}),200

@roles_accepted('Admin')
@auth_required('token')
@app.delete('/admin/albums/delete/<int:id>')
def delete_album(id):
    album_todel = Albums.query.filter_by(album_id=id).first()
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


@roles_accepted('Admin')
@auth_required('token')
@app.post('/admin/flag/<int:id>')
def flag(id):
    song = Songs.query.filter_by(song_id = id).first()
    song.flagged = not(song.flagged)
    db.session.commit()
    cache.clear()
    return jsonify({"message":"Song Flagged"}),200

