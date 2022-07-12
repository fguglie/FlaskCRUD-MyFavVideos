from cgitb import html
from multiprocessing.dummy import Array
from pydoc import Helper
from typing import List
from flask import redirect, url_for
from app import session, relativedelta,datetime, render_template, flash, generate_password_hash
from app.controller import user_controller, video_controller
from ..models.models import Video, User
from ..helpers import helper
from ..database import user_db, video_db
from config import Config

'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                    VIEWS HANDLERS (FOR GET PETTITIONS)                                      #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''

# Function to handle the validations of the main page for the route "/"
def index_handler()->redirect:
    # I instantiate the user object, and assign to it the session ID:
    user = User(id_usuario= session.get("id",False))

    # Checks if the user is logged in to redirect to the main page (if is not logged in) with an exception:
    helper.check_if_user_is_not_logged_in()



# Function to hanlde the validations of the login page for the route "/login"
def login_handler()->redirect:
    # Checks if the user is not logged in to redirect to the video panel with an exception:
    helper.check_if_user_is_not_logged_in()
    return redirect('/login')



# Function to hanlde the validations of the logout page for the route "/logout"
def logout_handler()->redirect:
    # I make the logout for the user, and redirect it to the index page:
    logout()

    # I set the message and status to return:
    message     = "Has cerrado la sesión correctamente."
    status      = "success"
    # I set the flash message:
    flash(message, status)
    return redirect('/')



# Function to hanlde the validations of the register page for the route "/registrarse"
def register_handler()->redirect:
    # Checks if the user is logged in to redirect to the main page (if is not logged in) or to the video panel:
    helper.check_if_user_is_logged_in()



# Function to hanlde the validations of editing own profile page for the route "/editar_perfil"
def edit_profile_handler()->User:
    # I instantiate the user object, and assign to it the session ID:
    user = User(id_usuario= session.get("id",False))

    # I check if the user is logged in:
    helper.check_if_user_is_logged_in()
    
    # I check if the user is trying to edit his own data:
    helper.check_if_user_is_editing_his_own_data(user)

    # I get the data of the user:
    return user_db.get_by_id(user)



# CORREGIR QUE NO USA LOS HELPERS
# Function to hanlde the validations of the "my videos" page for the route "/misvideos"
def list_my_videos_handler()->Video and List:
    # Checks if the user is logged in to redirect to the main page (if is not logged in) or to the video panel:
    helper.check_if_user_is_logged_in()

    # I instantiate the user object, and assign to it the ID of the current user, to get the videos of that user later:
    video = Video(id_usuario=int(session['id']))

    # I pass the user to the controller, to later get the videos of the current user:
    videos = video_controller.get_all_by_user_id(video)

    # I pass the list of videos to the global controller to set the DateTime differences:
    differences_between_dates = set_date_diff(videos)

    # I return the videos and the differences between dates to the route:
    return videos, differences_between_dates


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                      PROCESS POST REQUESTS FUNCTIONS                                        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''

# Function to process the uer login:
def login(user: User):
    # I check if the user exists:
    helper.check_login(user)

    # I check if the password is valid:
    helper.check_password(user)

    # I set the session parameters from the user who is logging in:
    user_controller.set_session(user)

    # I set the message and status to return:
    message     = f"Bienvenido {session['nombre']}!"
    status      = "success"

    # I set the flash message:
    flash(message, status)

    return None



# Function to search and store video from Youtube:
def search_and_store_video(video: Video) -> Video:

    # I fetch the Youtube video ID from the url entered:
    video_id = getattr(video_controller.get_youtube_video_id_from_url(video),"id_video_youtube")
    
    # I add to the video object the Youtube video ID fetched and the ID of the user who is fetching it:
    if hasattr(video, 'id_usuario'):
        video = video._replace(id_video_youtube= video_id)
    else:
        video = video._replace(id_video_youtube= video_id, id_usuario= session.get("id"))

    # I call the helper to check if the video exists for that user:
    helper.video_already_exists_for_user(video)

    # I fetch the video data from the youtube API:
    video_fetched = video_controller.get_youtube_video_data(video)

    # Now that I have all the data, i store it on the database:
    video_controller.save(video_fetched)

    # I return the video fetched:
    return video_fetched


# Function to process the user register:
def register_handler(user: User) ->None:

    # I send the user to the user controller to create the user:
    user_controller.user_create_handler(user)

    # I set the session parameters from the user who is signing in:
    user_controller.set_session(user)

    # I set the flash message:
    message     = f"Bienvenido {session['nombre']}!"
    status      = "success"
    flash(message, status)

    return None


# Function to process the self user profile update:
def edit_self_profile(user: User) ->None:
    # I check if the user is logged in:
    helper.check_if_user_is_logged_in()

    # I check if the user is trying to edit his own data:
    helper.check_if_user_is_editing_his_own_data(user)

    # ADD_HELPER
    # I check if the user data received is valid



    # I encript the password received and add to the object:
    if not user.clave == None:
        encrypted_password    = generate_password_hash(user.clave)
        user = user._replace(clave= encrypted_password)

    # I save the picture in the DB:
    user_db.update(user)

    # I save the picture (if it was received):
    if not user.foto_data == None:
        user.foto_data.save(Config.USER_IMAGES_FOLDER+user.foto)

    # I set the session parameters, to refresh the session data:
    user_controller.set_session(user)

    # I set the flash message:
    message     = f"Has actualizado tu usuario correctamente!"
    status      = "success"
    flash(message, status)

    return None
    
'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                           ADDITIONAL FUNCTIONS                                              #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''

# Function to calculate the difference between the date of publication of the video and the actual date in hours, days, months or, years:
def set_date_diff(videos: List[Video]) ->Array:

    #I generate the array for the dates:
    diferenciasDeFechas = []

    # I iterates between the videos:
    for video in videos:
        # I set the actual datetime:
        fechaActual = datetime.today()

        # I calculate the difference between the actual datetime and the date of publication of the video: 
        diff = relativedelta.relativedelta(fechaActual, video[6])

        # I set the variables for years, months, days and hours:
        años = diff.years
        meses = diff.months
        dias = diff.days
        horas = diff.hours

        #I assign the correct string for the date difference as appropriate:
        if años >=1:
            diferenciaDeFecha = "Hace "+str(años)+" año"
            if años >=2:
                diferenciaDeFecha = "Hace "+str(años)+" años"
        elif meses >=1:
            diferenciaDeFecha = "Hace "+str(meses)+" mes"
            if meses >=2:
                diferenciaDeFecha = "Hace "+str(meses)+" meses"
        elif dias >=1:
            diferenciaDeFecha = "Hace "+str(dias)+" dia"
            if dias >=2:
                diferenciaDeFecha = "Hace "+str(dias)+" dias"
        elif horas >=1:
            diferenciaDeFecha = "Hace "+str(horas)+" hora"
            if horas >=2:
                diferenciaDeFecha = "Hace "+str(horas)+" horas"

        # I add the date difference to the array:
        diferenciasDeFechas.append(diferenciaDeFecha)

    # I return all the date differences for all the videos in the list:
    return diferenciasDeFechas



# Function to make the logout of the application:
def logout()->None:
    session.clear()




    

