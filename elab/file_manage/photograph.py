from .base import FileBase
from flask_uploads import UploadSet,IMAGES
from flask import url_for

class Photograph(FileBase):
    def set_access(self):
        access=url_for('root.api.user.get_photograph',filename='',_external=True)
        access+='{}'
        self.access=access

photographs=Photograph(UploadSet('photographs', IMAGES),None)

