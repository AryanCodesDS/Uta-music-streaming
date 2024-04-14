from celery import shared_task
from application.models import User, Role ,User_track,Songs, Albums
from jinja2 import Template
from application.mailservices import send_message
from datetime import date 

file_path = "application/mail.html"
report_path = "application/report.html"
current_date = date.today()

@shared_task(ignore_result=False)
def monthly_reminder(to , subject):
    users = User.query.filter(User.roles.any(Role.name == 'Creator')).all()
    for user in users:
        song_count = len(Songs.query.filter_by(creator= user.user_id).all())
        album_count = len(Albums.query.filter_by(creator= user.user_id).all())
        user_rates= 0
        songs = Songs.query.filter_by(creator= user.user_id).order_by(Songs.ratings.desc()).all()
        highest_rated_songs = []
        for u in songs:
            if u.ratings >= 4 and len(highest_rated_songs) <= 5:
                highest_rated_songs.append(u)
            user_rates += u.user_rate_count
        with open(report_path, 'r') as f:
            template = Template(f.read())
            send_message(user.email, subject,template.render(song_count=song_count,album_count=album_count,rating_count=user_rates,highest_rated_songs=highest_rated_songs,name =user.name))
    return "Report Sent"


@shared_task(ignore_result=False)
def daily_reminder(to, subject):
    users = User.query.filter(User.roles.any(Role.name == 'General')).all()
    for user in users:
        user_last_login = User_track.query.filter_by(user_id = user.user_id).first().last_login
        if user_last_login != current_date and user_last_login != None:
            with open(file_path, 'r') as f:
                template = Template(f.read())
                send_message(user.email, subject,template.render(username =user.name))
                return "Reminder Sent"
        return "Not Sent" 