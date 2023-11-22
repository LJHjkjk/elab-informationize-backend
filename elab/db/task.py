from db import sqlAlchemy as db


class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)

    handler_id=db.Column(db.Integer)
    handler_name=db.Column(db.String)
   
    initiator_id=db.Column(db.Integer)
    initiator_name=db.Column(db.String(30))
    initiator_datetime=db.Column(db.DataTime)


    task_type=db.Column(db.Enum())
    associated_service_id=db.Column(db.String())
    