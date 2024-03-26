#imports
from flask import Flask
from flask_security import Security
from application.security import datastore
from werkzeug.security import generate_password_hash as hash
from application.models import db,User,Role
from application.resources import api
from flask_cors import CORS
from config import DevConfig
app = Flask(__name__,static_folder = './static',template_folder="./templates" )

#initializing the app and related modules.
with app.app_context():
    app.config.from_object(DevConfig)
    db.init_app(app)
    db.create_all()
    CORS(app,support_credentials=True)
    api.init_app(app)
    security = Security(app,datastore)
    datastore.find_or_create_role(name="General")
    datastore.find_or_create_role(name="Creator")
    datastore.find_or_create_role(name="Admin")
    db.session.commit()
    if not datastore.find_user(email = "admin@example.com"):
        datastore.create_user(email ="admin@example.com",password=hash("Admin@123"),roles=["Admin"],username="Admin_main@123",name="Admin_Main",active=True)
    db.session.commit()
    #except:
    print("Initial database already exists")
    #search.init_app(app)
    import application.views
    
    

if __name__ == "__main__":
    app.run(debug=True)