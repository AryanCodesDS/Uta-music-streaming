from models import User,Songs,Albums,Roles_Users,User_track,Albums,Playlists,Role
from sqlalchemy_data_model_visualizer import generate_data_model_diagram,add_web_font_and_interactivity

models = [User,Songs,Albums,Roles_Users,User_track,Albums,Playlists,Role]
generate_data_model_diagram(models,"diagram")
add_web_font_and_interactivity('diagram.svg', 'interactive_diagram.svg')