from .base import FileBase
from flask_uploads import UploadSet,IMAGES
from flask import url_for

class Avatar(FileBase):
    def set_access(self):
        access=url_for('static',filename='avatars/',_external=True)
        access+='{}'
        self.access=access

avatars=Avatar(UploadSet('avatars', IMAGES),None)

