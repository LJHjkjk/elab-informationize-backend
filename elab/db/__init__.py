from elab.extensions import sqlAlchemy


def init_db():
    from .user import init_user
    from .permission import init_permission
    from .mail import init_mail
    from .material import init_material
    from.file import init_file
    init_permission()
    init_user()
    init_mail()
    init_material()
    init_file()


def drop_db():
    from .user import drop_user
    from .permission import drop_permission
    from .mail import drop_mail
    from .material import drop_material
    from .file import drop_file
    drop_user()
    drop_permission()
    drop_mail()
    drop_material()
    drop_file()

def forge_db():
    from .permission import forge_permission
    from .user import forge_user
    from .mail import forge_mail
    from .material import forge_material
    from .file import forge_file
    forge_permission()
    forge_user()
    forge_mail()
    forge_material()
    forge_file()