from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    #engine = create_engine('sqlite:///Bankdb.db', echo=True)

    #Session = sessionmaker(bind=engine)
    #session = Session()
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Hospital.db'

    db.init_app(app)
    with app.app_context():

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        from .models import userstore

        @login_manager.user_loader
        def load_user(user_id):
            return userstore.query.get(str(user_id))
    
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from main import main as main_blueprint
        app.register_blueprint(main_blueprint)
        db.create_all() 
    
        return app
