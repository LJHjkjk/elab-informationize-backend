from flask import Blueprint

from .api import api_blueprint


blueprint=Blueprint('root',__name__)
blueprint.register_blueprint(api_blueprint,url_prefix='/api')
