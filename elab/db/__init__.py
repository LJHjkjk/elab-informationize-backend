from elab.extensions import mongodb,sqlAlchemy


def init_db():
    from .user import init_user
    init_user()

def drop_db():
    from .user import drop_user
    drop_user()

def forge_db():
    from .user import forge_user
    forge_user()