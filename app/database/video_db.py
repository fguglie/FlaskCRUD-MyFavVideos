from typing import List

from app.database.user_db import get_by_id
from .connection import _fetch_one, _fetch_all

# from .connection import _fetch_all
from ..models.models import Video, User
from ..models.exceptions import VideoNotValid, UserNotValid



# Function to create a video:
def save(video: Video) -> Video:
    
    #I generate the query and the parameters:
    query         = "INSERT INTO videos (thumbnail, titulo, url, canal, fecha_publicacion, visitas, likes, id_usuario, id_video_youtube) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    parameters    = (video.thumbnail, video.titulo, video.url, video.canal, video.fecha_publicacion, video.visitas, video.likes, video.id_usuario, video.id_video_youtube)

    # I execute the query
    video = _fetch_one(query,parameters)

    # Return the video inserted:
    return video




# Function to update a video:
def update(video: Video) -> Video:
    
    #I generate the query and the parameters:
    sql         = "UPDATE videos SET imagen = %s, titulo = %s, url = %s, canal = %s, fecha_publicacion = %s, visitas = %s, likes = %s, id_usuario = %s WHERE id_video = %s;"
    parameters  = (video.thumbnail, video.titulo, video.url, video.canal, video.fecha_publicacion, video.visitas, video.likes, video.id_usuario, video.id_video)

    # I execute the query
    video = _fetch_one(sql,parameters)

    # Return the video updated:
    return video



# Function to delete a video:
def delete(video: Video) -> Video:

    #I generate the query and the parameters:
    query       = "DELETE FROM videos WHERE id_video = %s"
    parameters  = (video.id_video)
    
    # Return the query executed:
    return _fetch_one(query,parameters)



# Function to get all videos:
def get_all() -> List[Video]:

    #I generate the query and the parameters:
    sql         = "SELECT * FROM videos"
    
    # I execute the query
    videos = _fetch_all(sql)

    # Return the video inserted:
    return videos




# Function to get details of one video:
def get_by_id(video: Video) -> Video:

    #I generate the query and the parameters:
    sql         = "SELECT * FROM videos WHERE id_video = %s"
    parameters  = (Video.id_video)

    # I execute the query
    video = _fetch_one(sql,parameters)

    # Return the video inserted:
    return video


# Function to get all videos by user_id:
def get_all_by_user_id(video: Video) -> List[Video]:

    #I generate the query and the parameters:
    sql         = "SELECT * FROM videos WHERE id_usuario = %s"
    parameters  = (video.id_usuario)

    # I execute the query
    videos = _fetch_all(sql, parameters)

    # Return the video inserted:
    return videos





# Function to validate if a video exists
def video_exists(video: Video) -> bool:
    query       = "SELECT * FROM videos WHERE id_video_youtube = %s AND id_usuario = %s"
    parameters       = (video.id_video_youtube, video.id_usuario)

    video = _fetch_one(query, parameters)
    return bool(video)