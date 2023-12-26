from elab.db.log import db
from datetime import datetime

class MaterialLog(db.Model):
    __tablename__='material_log'

    id=db.Column(db.Integer,primary_key=True)
    datetime=db.Column(db.DateTime, default=datetime.now())
    operation=db.Column(db.Enum('出库','入库'))
    operator_name=db.Column(db.String(100))
    operator_id=db.Column(db.String(100))
    operation_object_name=db.Column(db.String(100))
    operation_object_id=db.Column(db.Integer)
    old_number=db.Column(db.Integer)
    new_number=db.Column(db.Integer)
    change=db.Column(db.Integer)

    def return_to_dict(self):
        result={
            'id':self.id,
            'datetime':self.datetime.timestamp() if self.datetime else None,
            'operation':self.operation,
            'operator_id':self.operator_id,
            'operator_name':self.operator_name,
            'operation_object_name':self.operation_object_name,
            'operation_object_id':self.operation_object_id,
            'old_number':self.old_number,
            'new_number':self.new_number,
            'change':self.change,
        }
        return result


def init_material_log():
    db.metadata.create_all(bind=db.engine, tables=[MaterialLog.__table__])
    
def drop_material_log():
    try:
        db.session.execute(db.text('drop table if exists material_log'))
    except Exception as e:
        print(e)

def forge_material_log():
    pass