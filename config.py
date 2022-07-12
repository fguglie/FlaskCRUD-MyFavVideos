import os
from dotenv import load_dotenv

# Load the .env variables
load_dotenv()

class Config:
    SERVER_NAME             = "localhost:5000"
    DEBUG                   = True
    MYSQL_DATABASE_PASSWORD = os.environ.get("DB_PASS","")
    TEMPLATE_FOLDER         = "views/templates/"
    STATIC_FOLDER           = "views/static/"
    USER_IMAGES_FOLDER      = "app/views/static/img/users/"
    LOG_FOLDER              = 'app/logs/'
    MYSQL_DATABASE_HOST     = '127.0.0.1'
    MYSQL_DATABASE_USER     = 'root'
    MYSQL_DATABASE_DB       = 'tpo2python'
    YOUTUBE_API_KEY         = os.environ.get("YOUTUBE_API_KEY","")
    YOUTUBE_API_URL         = "https://www.googleapis.com/youtube/v3/videos"
    SECRET_KEY              = os.environ.get("SECRET_KEY","super secret key")
    LOG_LEVEL               = 'DEBUG'