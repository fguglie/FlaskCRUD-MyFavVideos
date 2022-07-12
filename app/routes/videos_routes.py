from app import request, session, flash, redirect, os, Blueprint, render_template
from ..controller import video_controller, user_controller, global_controller
import logging
from ..models.models import Video, User

#I define the blueprint videos as global_scope
videos = Blueprint("videos", __name__)

# I define the variable log to log the application events:
log = logging.getLogger(__name__)

#Route for viewing all videos, or videos by user ID (Only for Admin):
@videos.route("videos", methods=['GET'])
def get_videos():

    # I create a video object without parameters
    video = Video(id_usuario=None)

    # I ask to the video controller to get all the videos, or if it was specified, the videos from the user:
    videos = video_controller.get_videos(video)

    # I fetch all the users to later show them on the drop down list:
    users = user_controller.get_all_users()

    # I return the users and videos list to the video index view:
    return render_template('videos/index.html',videos=videos, users=users, title="Panel de Videos")




#Route for creating video (Only for Admin):
@videos.route("/videos/crear", methods=['GET'])
def video_create_view_handler():
    log.info(f'User {session.get("email",False) or "Unknown"} asked for route "/admin/videos/crear"')
    # I call the controller to hanlde the videos creation panel request:
    video_controller.video_create_view_handler()

    # I get all the users to display them on the dropdown:
    users = user_controller.get_all_users()

    # I return the videos list to the video index view:
    return render_template('videos/create.html', users=users, title="Crear nuevo video:")



#Route for editing a video (Only for Admin):
@videos.route("/videos/editar/<int:id>", methods=['GET'])
def video_edit_view_handler(id):
    log.info(f'User {session.get("email",False) or "Unknown"} asked for route "/admin/videos/editar/{id}"')
    # I create a video object which later I'm going to pass to the handler to fetch the video data:
    video = Video(id_video= id)

    # I call the controller to hanlde the video edit panel requested:
    video = video_controller.video_edit_view_handler(video)

    # I return the video data to the video edit view:
    return render_template('videos/edit.html',video=video, title="Editar video")

'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                PETITIONS HANDLERS OF THE SITE ROUTES (POSTS)                                #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''

#Route for viewing all videos of a specific user (Only for Admin):
@videos.route("videos/", methods=['POST'])
def get_videos_by_user_id():
    # Generate the variable id_usuario from the ID received:
    id_usuario        = request.form['id_usuario']    or None

    # I create a video object with the user ID
    video = Video(id_usuario= id_usuario)

    print(f"Video = {video}")
    # I ask to the video controller to get all the videos, or if it was specified, the videos from the user:
    videos = video_controller.get_videos(video)

    # I fetch all the users to later show them on the drop down list:
    users = user_controller.get_all_users()

    # I return the users and videos list to the video index view:
    return render_template('videos/index.html',videos=videos, users=users, title="Panel de Videos")



#Route for creating video (Only for Admin):
@videos.route("/videos/crear", methods=['POST'])
def video_create_handler():
    # I instantiate the video object, and assign to it the url of the Youtube video, which I have received from the request form:
    video = Video(url=request.form['url'], id_usuario= request.form['id_usuario'])
    
    log.info(f'User {session.get("email",False) or "Unknown"} sent a POST to route "/admin/videos/crear"')

    # I pass the video to the controller, to get the video data from the Youtube API and later store it on the DB:
    global_controller.search_and_store_video(video)

    # I return the user to the admin videos view panel, by flashing the success message:
    mensaje     = "Video agregado correctamente!"
    estado      = "success"
    flash(mensaje, estado)
    return redirect('/admin/videos')



#Route for editing a video (Only for Admin):
@videos.route("/videos/editar/<int:id>", methods=['POST'])
def video_edit_handler(id):
    log.info(f'User {session.get("email",False) or "Unknown"} sent a POST to route "/admin/videos/editar/{id}"')
    # I create a video object which later I'm going to pass to the handler to fetch the video data:
    video = Video(id_video= id)

    # I call the controller to hanlde the video edit panel requested:
    video = video_controller.video_edit_view_handler(video)

    # I return the video data to the video edit view:
    return render_template('videos/edit.html',video=video, title="Editar video")



#Route for deleting a video (Only for Admin):
@videos.route("/videos/borrar/<int:id>", methods=['POST'])
def video_delete_handler(id):
    log.info(f'User {session.get("email",False) or "Unknown"} is trying to delete a video in route "/admin/videos/borrar/{id}"')
    # I create a video object which later I'm going to pass to the handler to fetch the video data:
    video = Video(id_video= id)

    # I call the controller to hanlde the video edit panel requested:
    video = video_controller.delete_video(video)

    # I return the user to the admin videos view panel, by flashing the success message:
    mensaje     = "Video borrado correctamente!"
    estado      = "success"
    flash(mensaje, estado)

    # I return the video data to the video edit view:
    return redirect('/admin/videos')
















# #------------------------------------------------------Guardar/Borrar/Editar/Traer User------------------------------------------------------
# @users.route('/users/<int:id>',methods = ['GET', 'POST'])

# def user(id):

#     #Si es un POST:
#     if request.method == 'POST':

#         #Traigo el action para validar que acción se realizará (Delete, Create o Update)
#         action     = request.form['action']

#         #Si la acción es DELETE, entonces realizo el borrado
#         if action == "delete":
#             sql         = "DELETE FROM users WHERE id_usuario = %s;"
#             datos       = (id)
#             conn        = mysql.connect()
#             cursor      = conn.cursor()
#             cursor.execute(sql,datos)
#             conn.commit()
#             mensaje = "User Borrado Satisfactoriamente"
#             estado      = "success"

#         #Si es una creación, registro u edición de user: 
#         elif action == "create" or action == "update" or action == "registroUsuario":
#             #Asigno las variables
#             nombre      = request.form['nombre']
#             apellido    = request.form['apellido']
#             email       = request.form['email']
#             perfil       = request.form['perfil']

#             #Asigno las variables de acuerdo a si mandó o no la foto en el post
#             if not request.files['foto']:
#                 foto = 0
#                 nombreFoto  = "default.png"
#             else:
#                 foto        = request.files['foto']
#                 nombreFoto  = email+".jpg"
#                 foto.save("img/users/"+nombreFoto)  

#             #Si es el mismo user el que está editando sus datos, asigno la foto nueva a la variable de sesión para que se actualice en el header también:
#             if session["id"] == id:
#                 session["foto"] == nombreFoto

#             #Valido la acción para determinar si es una creación o una edición:
#             if action == "create" or action == "registroUsuario":
#                 password    = generate_password_hash(request.form['password'])
#                 sql         = "INSERT INTO users (nombre, apellido, email, foto, clave, administrador) VALUES (%s,%s,%s,%s,%s,%s);"
#                 datos       = (nombre, apellido, email, nombreFoto, password, perfil)
#                 if action == "registroUsuario":
#                     mensaje     = "Te has registrado satisfactoriamente!"
#                 else:
#                     mensaje     = "User creado satisfactoriamente!"
#                 estado      = "success"

#             elif action == "update":
#                 idUsuario     = request.form['idUsuario']
#                 #Si envió la password, la agrego a la consulta para actualizarla, si no, no cambio la password.
#                 if request.form['password']:
#                     password    = generate_password_hash(request.form['password'])
#                     #Valido si la foto existe, para que si es un update y no subió una nueva, no deje la default.
#                     if os.path.isfile("./img/users/"+nombreFoto) and not nombreFoto == 'default.png':
#                         sql= "UPDATE users SET nombre = %s, apellido = %s, email = %s, foto = %s, clave = %s, administrador = %s WHERE id_usuario = %s;"
#                         datos       = (nombre, apellido, email, nombreFoto, password, perfil, idUsuario)
#                     else:
#                         sql= "UPDATE users SET nombre = %s, apellido = %s, email = %s, clave = %s, administrador = %s WHERE id_usuario = %s;"
#                         datos       = (nombre, apellido, email, password, perfil, idUsuario)
#                 else:
#                     #Valido si la foto existe, para que si es un update y no subió una nueva, no deje la default.
#                     if os.path.isfile("./img/users/"+nombreFoto) and not nombreFoto == 'default.png':
#                         sql= "UPDATE users SET nombre = %s, apellido = %s, email = %s, foto = %s, administrador = %s WHERE id_usuario = %s;"
#                         datos       = (nombre, apellido, email, nombreFoto, perfil, idUsuario)
#                     else:
#                         sql= "UPDATE users SET nombre = %s, apellido = %s, email = %s, administrador = %s WHERE id_usuario = %s;"
#                         datos       = (nombre, apellido, email, perfil, idUsuario)
#                 mensaje     = "User editado satisfactoriamente!"
#                 estado      = "success"
#             conn        = mysql.connect()
#             cursor      = conn.cursor()
#             cursor.execute(sql,datos)
#             conn.commit()

#         #Paso el mensaje por flash:
#         flash(mensaje, estado)

#         #Si es un registro, lo redirecciono al panel de videos:
#         if action == "registroUsuario":
#             return redirect('/misvideos')
#         else:
#             #Si es administrador, lo retorno al panel de users, si no, al panel de videos (Porque editó su propio user)
#             if session["admin"] == 1:
#                 #Redirecciono al panel de users:
#                 return redirect('/verusuarios')
#             else:
#                 return redirect('/misvideos')

#     #Si es un GET:
#     elif request.method == 'GET':

#         #Valido que tenga la sesión activa:
#         if session is None:
#             mensaje     = "Debes iniciar sesión primero!"
#             estado      = "error"
#             #Paso el mensaje por flash:
#             flash(mensaje, estado)         
#             return redirect('/login')
        
#         #Valido que sea administrador:
#         print("session['id']:")
#         print(session['id'])
#         print("id:")
#         print(id)
#         print("admin = 0?")
#         print(session['admin'] == 0)
#         print("not session['id'] == id:")
#         print(not session['id'] == id)
#         if session['admin'] == 0 and not int(session['id']) == int(id):
#             print("ENTRO ACA!")
#             mensaje     = "Acceso denegado."
#             estado      = "error"
#             #Paso el mensaje por flash:
#             flash(mensaje, estado)         
#             return redirect('/')

#         sql         = "SELECT * FROM users WHERE id_usuario= %s;"
#         datos       = (id)

#         conn        = mysql.connect()
#         cursor      = conn.cursor()
#         cursor.execute(sql,datos)
#         user    = cursor.fetchone()
#         conn.commit()

#         return render_template('users/edit.html', user=user)