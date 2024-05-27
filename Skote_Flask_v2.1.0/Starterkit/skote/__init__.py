from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager    


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] =b'_5#y2L"F4Q8z\n\xec]/'
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqllite"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager = LoginManager(app)
    login_manager.login_view= 'authentication.login'
    db.init_app(app)
    

    from .models import User
    with app.app_context():
        db.create_all()


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) 
    
    from .dashboards import dashboards
    
    from .authentication import authentication
    from .utility import utility    
    from .layouts import layouts

    app.register_blueprint(dashboards ,url_prefix="/")    
    app.register_blueprint(authentication ,url_prefix="/")   
    app.register_blueprint(utility ,url_prefix="/")       
    app.register_blueprint(layouts ,url_prefix="/")

    return app  