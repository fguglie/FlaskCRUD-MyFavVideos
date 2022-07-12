import logging
from app import Config

class Logger():
    log_level = getattr(logging, Config.LOG_LEVEL)
    logging.basicConfig(filename=Config.LOG_FOLDER+'app.log', level=log_level, format=f'%(asctime)s %(levelname)s\t[%(name)s:%(lineno)d(%(funcName)s)]: %(message)s')
    logging.getLogger('werkzeug').disabled = True