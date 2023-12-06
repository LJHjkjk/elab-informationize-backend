from elab.db import sqlAlchemy as db

# 职位
class Positon(db.Model):
    __tablename__='positon'
    name=db.Column(db.String(100),primary_key=True)
    displayname=db.Column(db.String(100),nullable=False)
    describe=db.Column(db.String(200))

# 职责
class Duty(db.Model):
    __tablename__='duty'
    name=db.Column(db.String(100),primary_key=True)
    displayname=db.Column(db.String(100),primary_key=True)
    describe=db.Column(db.String(200))


# 职务和职责映射表
class PositonDutyMap(db.Model):
    __tablename__='position_duty_map'
    id=db.Column(db.String(100),primary_key=True)
    position_name=db.Column(db.String(100),db.ForeignKey('positon.name',ondelete='CASCADE'),nullable=False,)
    duty_name=db.Column(db.String(100),db.ForeignKey('duty.name',ondelete='CASCADE'),nullable=False)



def init_permission():
    db.metadata.create_all(db.engine,tables=[Positon.__table__,Duty.__table__,PositonDutyMap.__table__])

def drop_permission():
    db.session.execute(db.text('drop tables if exists positon,duty,position_duty_map'))

def forge_permission():
    pass