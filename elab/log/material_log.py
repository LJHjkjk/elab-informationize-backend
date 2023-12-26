from elab.db.log.material_log import MaterialLog,db
from elab.log.base import LogBase

class Material(LogBase):
    @classmethod
    def add(cls,operation,operator_name,operator_id,operation_object_name,operation_object_id,new_numebr,change):
        new_material=MaterialLog(
            operation=operation,
            operator_name=operator_name,
            operator_id=operator_id,
            operation_object_name=operation_object_name,
            operation_object_id=operation_object_id,
            new_number=new_numebr,
            change=change if operation=='入库' else -change
        )
        new_material.old_number=new_material.new_number-new_material.change
        db.session.add(new_material)
        db.session.commit()
        
