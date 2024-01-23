from factories.app import create_app
from factories.celery import configure_celery

# Imported for type hinting
from flask import Flask
from celery import Celery

# app = Flask(__name__)

def create_full_app() -> Flask:
    app: Flask = create_app()
    cel_app: Celery = configure_celery(app)
    return app

# if __name__ == '__main__':
#     # TODO: Add swagger integration
#     # app.run(debug=True)  # important to mention debug=True
#     app = create_full_app()
#     app.run(host='0.0.0.0', port=5000)
#     # app.run()