from app import request, session, flash, redirect, os, Blueprint, render_template, Config
from pathlib import Path
from ..controller import video_controller
from ..controller import user_controller
import logging
from ..models.models import User, Video

#I define the blueprint users as global_scope
users = Blueprint("users", __name__)

# I define the variable log to log the application events:
log = logging.getLogger(__name__)

'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                        SITE PAGES RENDERS (GETS)                                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''

#Route for viewing all users (Only for Admin):
@users.route("/usuarios", methods=['GET'])
@users.route("/usuarios/", methods=['GET'])
def users_panel_view_handler():
    log.info(f'User {session.get("email",False) or "Unknown"} asked for route "/admin/usuarios"')
    # I call the controller to hanlde the users request:
    users = user_controller.users_panel_view_handler()
        
    # I return the users list to the user index view:
    return render_template('users/index.html',users=users, title="Panel de Usuarios")



#Route for creating user (Only for Admin):
@users.route("/usuarios/crear", methods=['GET'])
def user_create_view_handler():
    log.info(f'User {session.get("email",False) or "Unknown"} asked for route "/admin/usuarios/crear"')
    # I call the controller to hanlde the users creation panel request:
    user_controller.user_create_view_handler()

    # I return the users list to the user index view:
    return render_template('users/create.html', title="Crear nuevo usuario")



#Route for editing a user (Only for Admin):
@users.route("/usuarios/editar/<int:id>", methods=['GET'])
def user_edit_view_handler(id):
    log.info(f'User {session.get("email",False) or "Unknown"} asked for route "/admin/usuarios/editar/{id}"')
    # I create a user object which later I'm going to pass to the handler to fetch the user data:
    user = User(id_usuario= id)

    # I call the controller to hanlde the user edit panel requested:
    user = user_controller.user_edit_view_handler(user)

    # I return the user data to the user edit view:
    return render_template('users/edit.html',user=user, title="Editar usuario")



'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                PETITIONS HANDLERS OF THE SITE ROUTES (POSTS)                                #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''

#Route for creating a user (Only for Admin):
@users.route("/usuarios/crear", methods=['POST'])
def user_create():
    # I asign the variables from what I recived from post:
    name        = request.form['nombre']    or None
    surname     = request.form['apellido']  or None
    password    = request.form['password']  or None
    email       = request.form['email']     or None
    admin       = request.form['perfil']    or None
    picture     = request.files['foto']     or None
    
    # If the user didn't send the picture, I set it to None
    if not request.files['foto']:
        picture_name  = "default.png"
    else:
        picture_name  = email+".jpg"

    # I create an user object with all the variables received:
    user = User(nombre= name, apellido= surname, foto= picture_name, email=email, clave=password, administrador= admin, foto_data=picture)
    log.info(f'User {session.get("email",False) or "Unknown"} sent a user create POST. Data: {user}')

    # I call the login function from the global controller:
    user_controller.user_create_handler(user)

    # I return the user to the admin users panel:
    return redirect('/admin/usuarios')



#Route for editing a user (Only for Admin):
@users.route("/usuarios/editar/<int:id>", methods=['POST'])
def user_edit(id):
    # I asign the variables from what I recived from post:
    id_usuario  = id
    name        = request.form['nombre']    or None
    surname     = request.form['apellido']  or None
    password    = request.form['password']  or None
    email       = request.form['email']     or None
    admin       = request.form['perfil']    or None
    picture     = request.files['foto']     or None
    
    # If the user didn't send the picture but already has one previously uploaded, I set it to None
    if not request.files['foto'] and Path(Config.USER_IMAGES_FOLDER+email+".jpg").is_file():
        picture_name  = email+".jpg"
    elif request.files['foto']:
        picture_name  = email+".jpg"
    else:
        picture_name  = "default.png"
        

    # I create an user object with all the variables received:
    user = User(id_usuario= id_usuario, nombre= name, apellido= surname, foto= picture_name, email=email, clave=password, administrador= admin, foto_data=picture)
    log.info(f'User {session.get("email",False) or "Unknown"} sent a user edit POST. Data: {user}')

    # I call the login function from the global controller:
    user_controller.user_edit_handler(user)

    # I return the user to the admin users panel:
    return redirect('/admin/usuarios')



















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

#         #Si es un registro, lo redirecciono al panel de users:
#         if action == "registroUsuario":
#             return redirect('/misvideos')
#         else:
#             #Si es administrador, lo retorno al panel de users, si no, al panel de users (Porque editó su propio user)
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