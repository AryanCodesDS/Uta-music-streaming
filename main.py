#imports
from flask import Flask
from flask_security import Security
from application.security import datastore
from werkzeug.security import generate_password_hash as hash
from application.models import db,User,Role,User_track
from application.resources import api,cache
from flask_cors import CORS
from config import DevConfig
from application.worker import celery_init_app
from celery.schedules import crontab
from application.task import daily_reminder,monthly_reminder

app = Flask(__name__,static_folder = './static',template_folder="./templates" )

#initializing the app and related modules.
with app.app_context():
    app.config.from_object(DevConfig)
    db.init_app(app)
    db.create_all()
    CORS(app,support_credentials=True)
    cache.init_app(app)
    cache.clear()
    api.init_app(app)
    security = Security(app,datastore)
    datastore.find_or_create_role(name="General")
    datastore.find_or_create_role(name="Creator")
    datastore.find_or_create_role(name="Admin")
    db.session.commit()
    if not datastore.find_user(email = "admin@example.com"):
        datastore.create_user(email ="admin@example.com",password=hash("Admin@123"),roles=["Admin"],username="Admin_main@123",name="Admin_Main",active=True)
    db.session.commit()
    print("Initial database already exists")
    import application.views

celery_app = celery_init_app(app) 
@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*"),
        #crontab(hour=9,minute=30),  #9:30 every day of the week.
        daily_reminder.s('21f1001076@ds.study.iitm.ac.in', 'UTA - Daily App Visit Reminder'),
    )
    sender.add_periodic_task(
        crontab(minute="*"),
        #crontab(hour=9,minute=30,day_of_month="1"),  #9:30 every 1st of the month
        monthly_reminder.s('21f1001076@ds.study.iitm.ac.in', 'UTA - Monthly Report Reminder'),
    )

if __name__ == "__main__":
    debug = True
    app.run()