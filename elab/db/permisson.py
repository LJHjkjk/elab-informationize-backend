from db import sqlAlchemy as db


class Positon(db.Model):
    __tablename__='positon'
    name=db.Column(db.String(30),primary_key=True)
    displayname=db.Column(db.String(30),nullable=False)
    describe=db.Column(db.String(200))


class Duty(db.Model):
    __tablename__='duty'
    name=db.Column(db.String(30),primary_key=True)

class PositonDutyMap(db.Model):
    __tablename__='duty_user_map'
    id=db.Column(db.Integet,primary=True,autoincrement=True)
    position_name=db.Column(db.String(30),db.ForeignKey('positon.name',ondelete='CASCADE'),nullable=False,)
    duty_name=db.Column(db.String(30),db.ForeignKey('duty.name',ondelete='CASCADE'),nullable=False)

