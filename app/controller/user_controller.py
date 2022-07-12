from pydoc import Helper
from typing import List
from app import session, Config, urllib, generate_password_hash, flash
from ..helpers import helper
from ..models.models import User
from ..database import user_db


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                               MAIN FUNCTIONS                                                #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''
# Function to get all the users:
def get_all_users() -> List[User]:
    # Fetch the users list:
    users = user_db.get_all()

    # Return the users:
    return users

'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                    VIEWS HANDLERS (FOR GET PETTITIONS)                                      #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''

# Function to handle the validations of the admin user panel page for the route "/admin/usuarios"
def users_panel_view_handler() ->User[list]:
    # I Check if the user is logged in to redirect to the main page (if is not logged in) or to the video panel:
    helper.check_if_user_is_logged_in()

    # I Check if the user is admin:
    helper.check_if_user_is_admin()

    # I get the users from the DB:
    users = user_db.get_all()

    # I return all the users:
    return users



# Function to handle the validations of the admin user panel page, for editing a specific user in route "/admin/usuarios"
def user_edit_view_handler(user: User) ->User:
    # I Check if the user is logged in to redirect to the main page (if is not logged in) or to the video panel:
    helper.check_if_user_is_logged_in()

    # I Check if the user is admin:
    helper.check_if_user_is_admin()

    # I get the users from the DB:
    user = user_db.get_by_id(user)

    # I return all the users:
    return user



# Function to handle the validations of the admin user panel page, for editing a specific user in route "/admin/usuarios"
def user_create_view_handler() ->None:
    # I Check if the user is logged in to redirect to the main page (if is not logged in) or to the video panel:
    helper.check_if_user_is_logged_in()

    # I Check if the user is admin:
    helper.check_if_user_is_admin()

    # I create the return
    return None



'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                      PROCESS POST REQUESTS FUNCTIONS                                        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''
# Function to handle and process a user creation:
def user_create_handler(user) ->None:
    # I check if the user exists:
    helper.user_already_exists(user)

    # ADD_HELPER
    # I check if the user data received is valid


    # I encript the password (if it was received) and add to the object:
    if not user.clave == None:
        encrypted_password    = generate_password_hash(user.clave)
        user = user._replace(clave= encrypted_password)

    # I save the picture in the DB:
    user_db.save(user)

    # I save the picture (if it was received):
    if not user.foto_data == None:
        user.foto_data.save(Config.USER_IMAGES_FOLDER+user.foto)

    # I set the message and status to return:
    message     = "Usuario creado satisfactoriamente!"
    status      = "success"
    # I set the flash message:
    flash(message, status)

    return None



# Function to handle and process a user edit:
def user_edit_handler(user) ->None:
    # I check if the user exists:
    helper.user_already_exists(user)

    # ADD_HELPER
    # I check if the user data received is valid



    # I encript the password (if it was received) and add to the object:
    if not user.clave == None:
        encrypted_password    = generate_password_hash(user.clave)
        user = user._replace(clave= encrypted_password)

    # I update the user in the DB:
    user_db.update(user)

    # I save the picture (if it was received), and update it in the session if the user is editing his own data:
    if not user.foto_data == None:
        user.foto_data.save(Config.USER_IMAGES_FOLDER+user.foto)
        if(session.get("id",False) == user.id_usuario):
            print("NO SE PERO ENTRO ACA")
            session['foto'] = user.foto


    # I set the message and status to return:
    message     = "Usuario editado satisfactoriamente!"
    status      = "success"

    # I set the flash message:
    flash(message, status)

    return None




'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                           ADDITIONAL FUNCTIONS                                              #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''

# Function to set the session variable with the user data:
def set_session(user: User) -> User:

    # I get the user from his id (if it is setted) or email:
    if user.id_usuario or False:
        user_fetched=user_db.get_by_id(user)
    else:
        user_fetched=user_db.get_user_by_email(user)

    # I replace the user attributes:
    user = user._replace(id_usuario = user_fetched[0], nombre= user_fetched[1], apellido= user_fetched[2], foto= user_fetched[3], email= user_fetched[4], administrador= user_fetched[5])
    
    # I set the session attributes:
    session['id'] = user.id_usuario
    session['nombre'] = user.nombre
    session['apellido'] = user.apellido
    session['foto'] = user.foto
    session['email'] = user.email
    session['admin'] = user.administrador

    # Return user:
    return user