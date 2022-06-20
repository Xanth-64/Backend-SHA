from flask import Flask
from flasgger import Swagger

def create_app():
    app = Flask(__name__)

    app.config['SWAGGER'] = {
        'title': 'Backend de Sistema de Hipermedia Adaptativo Educativo',
    }
    swagger = Swagger(app)
     ## Initialize Config
    app.config.from_pyfile('config.py')

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"
    return app

