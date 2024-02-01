from elab.extensions import sqlAlchemy
from .user import init_user,drop_user,forge_user
from .permission import init_permission,drop_permission,forge_permission
from .mail import init_mail,drop_mail,forge_mail
from .material import init_material,drop_material,forge_material
from .file import init_file,drop_file,forge_file
from .log import init_log,drop_log,forge_log
from .signin import init_signup,drop_signup,forge_signup


def init_db():
    init_permission()
    init_user()
    init_mail()
    init_material()
    init_file()
    init_log()
    init_signup()

def drop_db():
    drop_user()
    drop_permission()
    drop_mail()
    drop_material()
    drop_file()
    drop_log()
    drop_signup()
def forge_db():
    forge_user()
    forge_mail()
    forge_material()
    forge_file()
    forge_log()
    forge_signup()
    forge_permission()