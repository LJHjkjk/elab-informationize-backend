from flask import Blueprint



service_blueprint=Blueprint('service',__name__)

from .material_manage import material_manage_init
from .signin_system import signin_init
material_manage_init(service_blueprint)
signin_init(service_blueprint)

def service_init(api_blueprint):
    api_blueprint.register_blueprint(service_blueprint,url_prefix='/service')


