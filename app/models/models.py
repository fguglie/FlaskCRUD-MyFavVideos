from datetime import datetime
from typing import NamedTuple, Optional


class Video(NamedTuple):

    id_video            : Optional[int]     =None
    id_usuario          : Optional[int]     =None
    id_video_youtube    : Optional[str]     =None
    url                 : Optional[str]     =None
    titulo              : Optional[str]     =None
    canal               : Optional[str]     =None
    fecha_publicacion   : Optional[datetime]=None
    visitas             : Optional[int]     =None
    likes               : Optional[int]     =None
    thumbnail           : Optional[str]     =None


class User(NamedTuple):
    id_usuario          : Optional[int]     =None
    nombre              : Optional[str]     =None
    apellido            : Optional[str]     =None
    foto                : Optional[str]     =None
    email               : Optional[str]     =None
    administrador       : Optional[int]     =None
    clave               : Optional[str]     =None
    foto_data           : Optional[str]     =None
