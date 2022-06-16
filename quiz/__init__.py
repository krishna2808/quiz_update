from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from quiz.config import Config
db = SQLAlchemy()

def create_app(config_class=Config):

    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)
    
    from quiz.users.routes import users
    from quiz.admin.routes import admin
    
    
    app.register_blueprint(users)
    app.register_blueprint(admin)
    
    return app 
    

