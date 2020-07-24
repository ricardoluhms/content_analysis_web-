import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
#from flask_babel import Babel, lazy_gettext as _l
#from elasticsearch import Elasticsearch
#from redis import Redis
#import rq
from caw_app.config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
#babel = Babel()

login_manager = LoginManager(); login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    ### Check Later: Elasticsearch and Redis  
    # app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
    #     if app.config['ELASTICSEARCH_URL'] else None
    # app.redis = Redis.from_url(app.config['REDIS_URL'])
    # app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)

    ### api folder and files needs to be modified
    from caw_app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    ## error folder and files needs to be modified
    from caw_app.errors import errors_bp
    app.register_blueprint(errors_bp, url_prefix='/errors')

    ## verify routes and html paths of 
    from caw_app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/login')
    
    ## verify routes and html paths of main - folder changed from general to main
    from caw_app.main import main_bp
    #app.register_blueprint(main_bp, url_prefix='/index')
    app.register_blueprint(main_bp, url_prefix='/index')

    ## add html files from framxework and adapt them - modify routes
    from caw_app.edit_review import edit_review_bp
    app.register_blueprint(edit_review_bp, url_prefix='/edit_review')

    ## add html files from framework and adapt them - modify routes
    from caw_app.manage_reviews import manage_reviews_bp
    app.register_blueprint(manage_reviews_bp, url_prefix='/manage_reviews')

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Content Analysis Web Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/caws.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Content Analysis Web startup')

    return app

from caw_app import models
