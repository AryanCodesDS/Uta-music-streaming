from flask import current_app as app,request,jsonify,make_response
from application.models import db
from werkzeug.security import check_password_hash as check_hash
from werkzeug.security import generate_password_hash as hash
from application.security import datastore

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
            response = make_response(jsonify({"authtoken": user.get_auth_token()}), 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            return jsonify({"error": "Invalid Password"}),400
    else:
        return jsonify({"error": " Not An Admin"}),400

