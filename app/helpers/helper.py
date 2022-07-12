import re
from app import session, check_password_hash
from ..models.models import Video, User
from ..models.exceptions import UserNotLoggedIn, UserHasActiveSession, VideoNotValid, UserNotExists, UserAlreadyExists, LoginFailed, AccessDenied
from ..database import user_db, video_db

# Function to check if the user is logged in:
def check_if_user_is_logged_in() ->None:
    if not session.get("id",False):
        raise UserNotLoggedIn("Debes iniciar sesión primero!")


# Function to check if the user is not logged in:
def check_if_user_is_not_logged_in() ->None:
    if session.get("id",False):
        raise UserHasActiveSession()


# Function to check if the user is editing his own data:
def check_if_user_is_editing_his_own_data(user: User) ->None:
    if getattr(user,"id_usuario") == session.get(id,False):
        raise AccessDenied("Acceso denegado.")


# Function to check if the user we are searching for the login exists:
def check_login(user: User) ->None:
    if not user_db.get_user_by_email(user):
        raise LoginFailed("Usuario o contraseña inválida")


# Function to check if the password of the user is correct:
def check_password(user: User) ->None:
    db_password = user_db.get_user_by_email(user)[6]
    if not check_password_hash(db_password,user.clave):
        raise LoginFailed("Usuario o contraseña inválida")


# Function to check if the video that the user wants to add already exists:
def video_already_exists_for_user(video: Video) ->None:
    if video_db.video_exists(video):
        raise VideoNotValid("El video ya se encuentra agregado a tu lista de videos!")


# Function to check if the user that is trying to register already exists:
def user_already_exists(user: User) ->None:
    if user_db.get_user_by_email(user) and session.get("email",False) == user:
        raise UserAlreadyExists("Ya existe un usuario con el email ingresado.")


# Function to check if the user is admin or not:
def check_if_user_is_admin() ->None:
    if not session.get("admin",False) == 1:
        raise AccessDenied("Acceso denegado.")









def validate_video(video: Video) -> None:

    # Valido que el id del video sea válido
    if not __video_id_is_valid(video.id_video_youtube):
        raise VideoNotValid(f"El id del video ingresado ({{video.id_video_youtube}}) no es válido")

    # Valido que los campos necesarios sean correctos
    if None in (video.id_usuario, video.url, video.titulo):
        raise VideoNotValid("El video no tiene un usuario asignado, una URL o Título")



def __video_id_is_valid(id: str) ->bool:
    # Defino la expresión regular para validar que no traiga el signo de pregunta
    regex = '^((?!?).)*$'

    #Valido si el ID del video no tiene la expresión
    return bool(re.search(regex, id))

