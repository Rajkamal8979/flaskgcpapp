

import logging

from flask import current_app, Flask, redirect, url_for


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)
    # Register the Bookshelf CRUD blueprint.
    from .crud import crud
    app.register_blueprint(crud)

    # Add a default root route.
    @app.route("/")
    def index():
        return redirect(url_for('crud.list'))
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app


# def get_model():
#     model_backend = current_app.config['DATA_BACKEND']
#     if model_backend == 'cloudsql':
#         from . import model_cloudsql
#         model = model_cloudsql
#     elif model_backend == 'datastore':
#         from . import model_datastore
#         model = model_datastore
#     elif model_backend == 'mongodb':
#         from . import model_mongodb
#         model = model_mongodb
#     else:
#         raise ValueError(
#             "No appropriate databackend configured. "
#             "Please specify datastore, cloudsql, or mongodb")
#
#     return model
