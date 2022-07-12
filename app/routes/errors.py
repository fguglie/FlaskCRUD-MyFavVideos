# from shutil import ExecError
from flask import jsonify, Blueprint, Response, session
from app import flash, redirect
from ..models.exceptions import AccessDenied, UserHasActiveSession, UserAlreadyExists, UserNotLoggedIn, UserNotExists, LoginFailed, VideoNotValid
import logging

# I define the variable log to log the application events:
log = logging.getLogger(__name__)

#I define the blueprint as errors:
errors = Blueprint("errors", __name__)

# Function to receive the error by the exception and generate the flash by it:
def __generate_error_response(error: Exception) -> flash:
    message     = str(error)
    status      = "error"
    return flash(message, status)


# Error handler for the user not logged in Exception:
@errors.app_errorhandler(UserNotLoggedIn)
def handle_global_exceptions(error: UserNotLoggedIn) -> redirect:
    __generate_error_response(error)
    log.error(f'User {session.get("email",False) or "Unknown"} is not logged in and tried to access a route in which has to be logged in first. Error: {error}')
    return redirect('/misvideos')



# Error handler for the user has active session Exception:
@errors.app_errorhandler(UserHasActiveSession)
def handle_global_exceptions(error: UserHasActiveSession) -> redirect:
    log.error(f'User {session.get("email",False) or "Unknown"} tried to access to a disabled view for active session. Error: {error}')
    return redirect('/misvideos')



# Error handler for the user already exists Exception:
@errors.app_errorhandler(LoginFailed)
def handle_global_exceptions(error: LoginFailed) -> redirect:
    __generate_error_response(error)
    log.error(f'User {session.get("email",False) or "Unknown"} entered an invalid user or password. Error: {error}')
    return redirect('/login')



# Error handler for the video not valid Exception:
@errors.app_errorhandler(VideoNotValid)
def handle_global_exceptions(error: VideoNotValid) -> redirect:
    __generate_error_response(error)
    log.error(f'User {session.get("email",False) or "Unknown"} tried to add a video that was already added to his playlist. Error: {error}')
    return redirect('/misvideos')



# Error handler for the access denied Exception:
@errors.app_errorhandler(AccessDenied)
def handle_global_exceptions(error: AccessDenied) -> redirect:
    __generate_error_response(error)
    log.error(f'User {session.get("email",False) or "Unknown"} tried to access a route without having the necessary permissions. Error: {error}')
    return redirect('/')



# Error handler for the user already exists Exception:
@errors.app_errorhandler(UserAlreadyExists)
def handle_global_exceptions(error: UserAlreadyExists) -> redirect:
    __generate_error_response(error)
    log.error(f'User {session.get("email",False) or "Unknown"} tried to register, but the user already exists. Error: {error}')
    return redirect('/login')