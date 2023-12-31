from .base import FileBase
from flask_uploads import UploadSet,IMAGES
from flask import url_for,current_app


class Photograph(FileBase):
    def set_access(self):
        access='http://'+current_app.config['ROOT_URL']+'/api/user/photograph/'
        access+='{}'
        self.access=access

photographs=Photograph(UploadSet('photographs', IMAGES),None)

