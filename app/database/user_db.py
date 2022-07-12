from tkinter.font import BOLD
from typing import List
from .connection import _fetch_one, _fetch_all
from ..models.models import User
from ..models.exceptions import UserNotValid


# Function to get all users:
def get_all() -> List[User]:

    #I generate the query and the parameters:
    sql         = "SELECT * FROM usuarios"
    
    # I execute the query
    users = _fetch_all(sql)

    # Return the video inserted:
    return users



# Function to get details of one user:
def get_by_id(user: User) -> User:

    #I generate the query and the parameters:
    sql         = "SELECT * FROM usuarios WHERE id_usuario = %s"
    parameters  = (user.id_usuario)

    # I execute the query
    user = _fetch_one(sql,parameters)

    # Return the user inserted:
    return user

def get_user_by_email(user: User) -> User:

    #I generate the query and the parameters:
    sql         = "SELECT * FROM usuarios WHERE email = %s"
    parameters  = (user.email)

    # I execute the query
    user = _fetch_one(sql,parameters)

    # Return the user inserted:
    return user

# Function to store a user:
def save(user: User) -> User:
    # query         = "INSERT INTO usuarios (nombre, apellido, foto, email, administrador, clave) VALUES (%s,%s,%s,%s,%s,%s);"
    # parameters    = (user.nombre, user.apellido, user.foto, user.email, user.administrador, user.clave)
    #I generate the query and the parameters (I iterates over the user data and if the value is none, i exlude it from the query):
    sql         = str("INSERT INTO usuarios (")
    sql2 = str(" (")
    parameters  = []
    for name, value in user._asdict().items():
        if not value == None and not name == "foto_data":
            sql+=str(name)+", "
            sql2+=str("%s,")
            parameters.append(value)
    
    sql = str(sql[:-2]+") VALUES")
    sql2 = str(sql2[:-1]+");")
    sql+=str(sql2)
    print(f"sql= {sql}")
    print(f"parameters= {parameters}")
    # sql = "UPDATE usuarios SET nombre= %s, apellido= %s, foto= %s, administrador= %s WHERE id_usuario = %s"
    # params = (user.nombre, user.apellido, user.foto, int(user.administrador), user.id_usuario)
    
    # I execute the query
    user = _fetch_one(sql,parameters)

    # Return the user updated:
    return user











    # #I generate the query and the parameters:
    # query         = "INSERT INTO usuarios (nombre, apellido, foto, email, administrador, clave) VALUES (%s,%s,%s,%s,%s,%s);"
    # parameters    = (user.nombre, user.apellido, user.foto, user.email, user.administrador, user.clave)

    # # I execute the query
    # user = _fetch_one(query,parameters)

    # # Return the user inserted:
    # return user



# Function to update a user:
def update(user: User) -> User:
    #I generate the query and the parameters (I iterates over the user data and if the value is none, i exlude it from the query):
    sql         = "UPDATE usuarios SET "
    parameters  = []
    for name, value in user._asdict().items():
        if not value == None and (not name == "id_usuario" and not name == "foto_data"):
            sql+=str(name)+"= %s, "
            parameters.append(value)
    
    sql = sql[:-2]+" WHERE id_usuario = %s;"
    parameters.append(user.id_usuario)

    print(f"sql={sql}")
    print(f"parameters={parameters}")
    # sql = "UPDATE usuarios SET nombre= %s, apellido= %s, foto= %s, administrador= %s WHERE id_usuario = %s"
    # params = (user.nombre, user.apellido, user.foto, int(user.administrador), user.id_usuario)
    
    # I execute the query
    user = _fetch_one(sql,parameters)

    # Return the user updated:
    return user