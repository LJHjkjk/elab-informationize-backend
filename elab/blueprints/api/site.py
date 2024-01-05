from flask import Blueprint,current_app
from elab.response import response_data,response_message

site_blueprint=Blueprint('site',__name__)



@site_blueprint.route('')
def get_site_info():
  return response_data(current_app.config['SITE_INFO'])




def site_init(api_blueprint):
  api_blueprint.register_blueprint(site_blueprint,url_prefix='/site')