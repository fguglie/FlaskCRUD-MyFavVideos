from app import request, session, flash, redirect, os, Blueprint, render_template
from ..controller import user_controller, video_controller, global_controller
from ..models.models import User, Video
import logging


# I define the variable log to log the application events:
log = logging.getLogger(__name__)

#I define the blueprint as global_scope
global_scope = Blueprint("global_routes", __name__)


'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                        SITE PAGES RENDERS (GETS)                                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''

# Route for render the index or main application page:
@global_scope.route("/", methods=['GET'])
def index() ->render_template:
    log.info(f'User {session.get("email",False) or "Unknown"} asked for route "/"')
    # I call the index handler, which is going to make all the verifications and redirects if there is any exception:
    global_controller.index_handler()
    return render_template('index.html', title="Home")


# Route for render the login page:
@global_scope.route('/login', methods=['GET'])
def render_login() ->render_template:
    log.info(f'User {session.get("email",False) or "Unknown"} asked for route "/login"')
    # I call the login handler, which is going to make all the verifications and redirects if there is any exception:
    global_controller.login_handler()
    return render_template('site_pages/login.html', title="Iniciar Sesión")



# Route for creating an account:
@global_scope.route('/registrarse', methods=['GET'])
def sign_in() ->render_template:
    log.info(f'User {session.get("email",False) or "Unknown"} asked for route "/registrarse"')
    global_controller.register_handler()
    return render_template('site_pages/registrarse.html', title="Registrarse")



# Route for the user video panel, in which are all the videos that he added to the favorite list:
@global_scope.route('/misvideos', methods=['GET'])
def list_my_videos() ->render_template:
    log.info(f'User {session.get("email",False) or "Unknown"} asked for route "/misvideos"')
    videos, diferenciasDeFechas = global_controller.list_my_videos_handler()
    # I return the template, and pass to it the list of videos and the DateTime differences:
    return render_template('videos/misvideos.html', videos=videos, diferenciasDeFechas=diferenciasDeFechas, title="Mis Videos")



# Route for application logout:
@global_scope.route('/logout', methods=['GET'])
def logout() ->render_template:
    log.info(f'User {session.get("email",False) or "Unknown"} asked for route "/logout"')
    global_controller.logout_handler()
    return render_template('index.html', title="Home")



# Route for editing own user:
@global_scope.route('/editarperfil', methods=['GET'])
def render_edit_profile() ->render_template:
    log.info(f'User {session.get("email",False) or "Unknown"} asked for route "/edit_profile"')
    user = global_controller.edit_profile_handler()

    if session.get("admin",False):
        return redirect('admin/usuarios/editar/'+str(session.get("id")))
    else:
        return render_template('users/edit.html', user=user, title="Editar Perfil")

'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                PETITIONS HANDLERS OF THE SITE ROUTES (POSTS)                                #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''

# Route for making an app login:
@global_scope.route('/login', methods=['POST'])
def login() ->redirect:
    # I create an object user with the values received from post:
    user = User(email=request.form['email'], clave=request.form['password'])
    
    log.info(f'User {session.get("email",False) or "Unknown"} asked to log in. User email: {user.email}')
    log.debug(f'User {session.get("email",False) or "Unknown"} asked to log in. User email: {user.email}, Password: {user.clave}')

    # I call the login function from the global controller:
    global_controller.login(user)

    # I return the user to "MyVideos" panel:
    return redirect('/misvideos')



# Route for making an app register:
@global_scope.route('/registrarse', methods=['POST'])
def register() ->redirect:
    # I asign the variables from what I recived from post:
    name        = request.form['nombre']
    surname     = request.form['apellido']
    password    = request.form['password']
    email       = request.form['email']
    admin       = 0
    foto_data   = request.files['foto'] or None
    
    # If the user didn't send the picture, I set it to None
    if not foto_data:
        picture_name  = "default.png"
    else:
        picture_name  = email+".jpg"

    # I create an user object with all the variables received:
    user = User(nombre= name, apellido= surname, foto= picture_name, email=email, clave=password, administrador= admin, foto_data=foto_data)
    log.info(f'User {session.get("email",False) or "Unknown"} sent a register POST. Data: {user}')

    # I call the login function from the global controller:
    global_controller.register_handler(user)

    # I return the user to the "MyVideos" panel:
    return redirect('/misvideos')



# Route for adding a video to the user videos list:
@global_scope.route('/misvideos', methods=['POST'])
def add_video() ->redirect:
    # I instantiate the video object, and assign to it the url of the Youtube video, which I have received from the request form:
    video = Video(url=request.form['link'], id_usuario=session["id"])
    
    log.info(f'User {session.get("email",False) or "Unknown"} asked to add a video: {video.url}')

    # I pass the video to the controller, to get the video data from the Youtube API and later store it on the DB:
    global_controller.search_and_store_video(video)

    # I return the user to the "MyVideos" panel, by flashing the success message:
    mensaje     = "Video agregado a tu lista!"
    estado      = "success"
    flash(mensaje, estado)
    return redirect('/misvideos')



# Route for making a self user update from the edit profile tab:
@global_scope.route('/editarperfil', methods=['POST'])
def edit_self_profile() ->redirect:
    # I asign the variables from what I recived from post:
    id      = session["id"]
    name    = request.form['nombre']
    surname = request.form['apellido']
    password= request.form['password'] or None
    admin   = request.form['perfil']
    picture = request.files['foto'] or None
    
    # If the user didn't send the picture, I set it to None
    if not picture:
        picture_name  = "default.png"
    else:
        picture_name  = session.get("email",False)+".jpg"

    # I create an user object with all the variables received:
    user = User(id_usuario= id, nombre= name, apellido= surname, foto= picture_name, clave=password, administrador= admin, foto_data=picture)
    log.info(f'User {session.get("email",False) or "Unknown"} sent a self user update POST. Data: {user}')

    # I call the login function from the global controller:
    global_controller.edit_self_profile(user)

    # I return the user to the "MyVideos" panel:
    return redirect('/misvideos')

















# #------------------------------------------------------Guardar/Borrar/Editar/Traer User------------------------------------------------------
# @usuarios.route('/usuarios/<int:id>',methods = ['GET', 'POST'])

# def user(id):

#     #Si es un POST:
#     if request.method == 'POST':

#         #Traigo el action para validar que acción se realizará (Delete, Create o Update)
#         action     = request.form['action']

#         #Si la acción es DELETE, entonces realizo el borrado
#         if action == "delete":
#             sql         = "DELETE FROM usuarios WHERE id_usuario = %s;"
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
#                 sql         = "INSERT INTO usuarios (nombre, apellido, email, foto, clave, administrador) VALUES (%s,%s,%s,%s,%s,%s);"
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
#                         sql= "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, foto = %s, clave = %s, administrador = %s WHERE id_usuario = %s;"
#                         datos       = (nombre, apellido, email, nombreFoto, password, perfil, idUsuario)
#                     else:
#                         sql= "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, clave = %s, administrador = %s WHERE id_usuario = %s;"
#                         datos       = (nombre, apellido, email, password, perfil, idUsuario)
#                 else:
#                     #Valido si la foto existe, para que si es un update y no subió una nueva, no deje la default.
#                     if os.path.isfile("./img/users/"+nombreFoto) and not nombreFoto == 'default.png':
#                         sql= "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, foto = %s, administrador = %s WHERE id_usuario = %s;"
#                         datos       = (nombre, apellido, email, nombreFoto, perfil, idUsuario)
#                     else:
#                         sql= "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, administrador = %s WHERE id_usuario = %s;"
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
#             #Si es administrador, lo retorno al panel de usuarios, si no, al panel de videos (Porque editó su propio user)
#             if session["admin"] == 1:
#                 #Redirecciono al panel de usuarios:
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

#         sql         = "SELECT * FROM usuarios WHERE id_usuario= %s;"
#         datos       = (id)

#         conn        = mysql.connect()
#         cursor      = conn.cursor()
#         cursor.execute(sql,datos)
#         user    = cursor.fetchone()
#         conn.commit()

#         return render_template('usuarios/edit.html', user=user)