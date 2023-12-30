from .base import FileBase
from flask_uploads import UploadSet,IMAGES
from flask import current_app,url_for

class Avatar(FileBase):
    def set_access(self):
        access='http://'+current_app.config['ELAB_SERVER_NAME']+'/api/static/avatars/'
        access+='{}'
        self.access=access

avatars=Avatar(UploadSet('avatars', IMAGES),None)

