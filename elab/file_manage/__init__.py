from .avatar import avatars
from .photograph import photographs

class FileManage():
    def __init__(self):
        self.sets=[
            avatars,
            photographs,
        ]

    def init_app(self,app):
        for i in self.sets:
            i.init_app(app)
    
    def set_access(self):
        for i in self.sets:
            i.set_access()

