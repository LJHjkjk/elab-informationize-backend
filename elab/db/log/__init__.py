from elab.db import sqlAlchemy as db


def init_log():
    from .material_log import init_material_log
    init_material_log()


def drop_log():
    from .material_log import drop_material_log
    drop_material_log()
    

def forge_log():
    from .material_log import forge_material_log
    forge_material_log()
    