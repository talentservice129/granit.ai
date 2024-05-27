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
    from .apps import apps
    from .ecommerce import ecommerce
    from .crypto import crypto
    from .email import email
    from .invoices import invoices
    from .projects import projects
    from .tasks import tasks
    from .contacts import contacts
    from .blogs import blogs
    from .jobs import jobs
    from .authentication import authentication
    from .utility import utility
    from .components import components
    from .layouts import layouts

    app.register_blueprint(dashboards ,url_prefix="/")
    app.register_blueprint(apps ,url_prefix="/")
    app.register_blueprint(ecommerce ,url_prefix="/")
    app.register_blueprint(crypto ,url_prefix="/")
    app.register_blueprint(email ,url_prefix="/")
    app.register_blueprint(invoices ,url_prefix="/")
    app.register_blueprint(projects ,url_prefix="/")   
    app.register_blueprint(tasks ,url_prefix="/")   
    app.register_blueprint(contacts ,url_prefix="/")   
    app.register_blueprint(blogs ,url_prefix="/")   
    app.register_blueprint(jobs ,url_prefix="/")   
    app.register_blueprint(authentication ,url_prefix="/")   
    app.register_blueprint(utility ,url_prefix="/")   
    app.register_blueprint(components ,url_prefix="/")
    app.register_blueprint(layouts ,url_prefix="/")

    return app  