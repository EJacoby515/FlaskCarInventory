from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app.config import Config
from app.api.routes import api
from app.site.routes import site
from app.authentication.routes import auth
from app.models import db as root_db, login_manager, ma
from app.helpers import JSONEncoder 
from flask_cors import CORS
from flask_migrate import Migrate 

db = SQLAlchemy()
app = Flask(__name__, static_url_path='/static')
CORS(app)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

app.json_encoder = JSONEncoder
app.config.from_object(Config)
root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)
