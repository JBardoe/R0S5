from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdfghjkl'

    from .auth import auth
    from .employee import employee

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(employee, url_prefix='/')

    return app

