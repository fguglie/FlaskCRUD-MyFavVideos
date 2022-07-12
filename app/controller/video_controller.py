from pydoc import Helper
from typing import List
from app import session, Config, urllib, json, request
from ..helpers import helper
from ..models.models import Video, User
from ..database import video_db




'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                    VIEWS HANDLERS (FOR GET PETTITIONS)                                      #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''



# Function to get videos for showing them on the admin video panel (Admin only!):
def get_videos(video: Video) -> List[Video]:
    # I check if the user is admin:
    helper.check_if_user_is_admin()

    # I check if the user is logged in:
    helper.check_if_user_is_logged_in()

    # If there is a user ID, I search for the videos of the user else i search all the videos for the specified user:
    if video.id_usuario is None or video.id_usuario == "All":
        videos = video_db.get_all()
    else:   
        videos = video_db.get_all_by_user_id(video)
    
    # I return all the videos fetched:
    return videos



# Function to handle the validations of the admin video panel page, for editing a specific video in route "/admin/videos/editar"
def video_edit_view_handler(video: Video) ->Video:
    # I Check if the video is logged in to redirect to the main page (if is not logged in) or to the video panel:
    helper.check_if_user_is_logged_in()

    # I Check if the video is admin:
    helper.check_if_user_is_admin()

    # I get the videos from the DB:
    video = video_db.get_by_id(video)

    # I return all the videos:
    return video



# Function to handle the validations of the admin user panel page, for editing a specific user in route "/admin/usuarios"
def video_create_view_handler() ->None:
    # I Check if the user is logged in to redirect to the main page (if is not logged in) or to the video panel:
    helper.check_if_user_is_logged_in()

    # I Check if the user is admin:
    helper.check_if_user_is_admin()

    # I create the return
    return None









'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                      SPECIFIC VIDEO FUNCTIONS                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''

# Function to save a specific video:
def save(video: Video) ->None:
    video_db.save(video)
    return None



# Function to fetch all videos from a specific user:
def get_all_by_user_id(video: Video) ->List[Video]:
    videos = video_db.get_all_by_user_id(video)
    return videos


# Function to delete a specific Video:
def delete_video(video: Video) -> None:
    video_db.delete(video)
    return None



# Function to get the Youtube video ID from Youtube:
def get_youtube_video_id_from_url(video: Video) -> Video:

    # I assign to the video object the id of the youtube video, which I have to split from the url of the video:
    video = video._replace(id_video_youtube=video.url.split('watch?v=',2)[1].split('&',2)[0], url=video.url)

    # ADD_HELPER:
    # I call the Helper to check if the ID of the youtube video has a correct syntax:



    # I return the video:
    return video



# Function to get the data of the video from the Youtube API:
def get_youtube_video_data(video: Video) -> Video:

    # I get the Youtube API key from the configuration file, which I'm going to need for search in the api.
    api_key = Config.YOUTUBE_API_KEY

    # I generate the params which I want to get from the video that I'm going to search:
    params = {'id': video.id_video_youtube, 'key': api_key,
            'fields': 'items(id,snippet(channelId,channelTitle,title,categoryId,thumbnails,publishedAt),statistics)',
            'part': 'snippet,statistics'}
    
    # I generate the variable with the youtube API URL:
    url = Config.YOUTUBE_API_URL

    # I generate the URL to which I'm going to make the query:
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    # I make the post to the Youtube API, read the response and assign it to the data variable:
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
    
    # ADD_HELPER:
    # I call the Helper to check if all the fields that I need were returned correctly from the Youtube API:



    # I assign the variables from the data received:
    titulo            = data['items'][0]['snippet']['title']
    canal             = data['items'][0]['snippet']['channelTitle']
    fecha_publicacion = data['items'][0]['snippet']['publishedAt']
    visitas           = int(data['items'][0]['statistics']['viewCount'])
    likes             = int(data['items'][0]['statistics']['likeCount'])
    thumbnail         = data['items'][0]['snippet']['thumbnails']['high']['url']

    # I assign the variables to the new object video:
    video = video._replace(titulo=titulo, canal=canal, fecha_publicacion=fecha_publicacion, visitas=visitas, likes=likes, thumbnail=thumbnail, id_video_youtube=video.url.split('watch?v=',2)[1].split('&',2)[0], url=video.url)
    
    # I return the video object searched:
    return video