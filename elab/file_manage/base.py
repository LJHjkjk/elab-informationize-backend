from flask_uploads import configure_uploads
from flask import current_app
import os

class FileBase:
    def __init__(self,uploadSet,access=None):
        # access是模版字符串
        self.uploadSet=uploadSet
        self.access=access

    def init_app(self,app):
        configure_uploads(app=app,upload_sets=self.uploadSet)

    def save(self,file):
        return self.uploadSet.save(file)
    
    def url(self,filename):
        if self.access:
            return self.access.format(filename)
        else:
            return None
    
    def path(self,filename,absolute=False):
        if absolute:
            return current_app.root_path+'/'+self.uploadSet.path(filename)
        else:
            return self.uploadSet.path(filename)
    

    def delete(self,filename):
        # 获取项目位置
        root_path=current_app.root_path
        # 得到文件绝对储存位置
        absolute_position=root_path+'/'+self.uploadSet.path(filename)
        # 查看是否存在
        try:
            os.remove(absolute_position)
        except Exception as e:
            print(e)

    def set_access(self):
        pass