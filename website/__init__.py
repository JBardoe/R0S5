from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdfghjkl'

    from .auth import auth
    from .employee import employee
    from .calendar import calendar

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(employee, url_prefix='/')
    app.register_blueprint(calendar, url_prefix='/')

    return app

