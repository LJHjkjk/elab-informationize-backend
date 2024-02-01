from elab.db import sqlAlchemy as db

# 职位
class Positon(db.Model):
    __tablename__='position'
    name=db.Column(db.String(100),primary_key=True)
    display_name=db.Column(db.String(100),nullable=False)
    describe=db.Column(db.String(1000))

    # 为职位添加整个类型的职责
    def add_duty_typied(self,type):
        if type=='*':
            dutys=Duty.query.all()
        else:
            dutys=Duty.query.filter_by(type=type).all()
        if len(dutys)==0:
            return 
        position_duty_map=[]
        for duty in dutys:
            position_duty_map.append(PositonDutyMap(position_name=self.name,duty_name=duty.name))
        db.session.add_all(position_duty_map)
        db.session.commit()

    # 为职位添加职责列表
    def add_dutys(self,dutys):
        if not dutys:
            return 
        dutys_list=[]
        for duty in dutys:
            dutys_list.append(Duty.query.get(duty))
        position_duty_map=[PositonDutyMap(position_name=self.name,duty_name=duty.name) for duty in dutys_list]
        db.session.add_all(position_duty_map)

    def return_to_dict(self):
        return{
            'name':self.name,
            'displayname':self.displayname,
            'describe':self.describe,
        }

# 职责
class Duty(db.Model):
    __tablename__='duty'
    name=db.Column(db.String(100),primary_key=True)
    type=db.Column(db.String(100))
    displayname=db.Column(db.String(100),primary_key=True)
    describe=db.Column(db.String(1000))


# 职务和职责映射表
class PositonDutyMap(db.Model):
    __tablename__='position_duty_map'
    position_name=db.Column(db.String(100),primary_key=True,nullable=False,)
    duty_name=db.Column(db.String(100),primary_key=True,nullable=False)


# 成员和职责映射表
class MemberDutyMap(db.Model):
    __tablename__='member_duty_map'
    member_id=db.Column(db.String(100),primary_key=True)
    duty=db.Column(db.String(100),primary_key=True)
    



def init_permission():
    db.metadata.create_all(db.engine,tables=[
        Positon.__table__,Duty.__table__,PositonDutyMap.__table__,MemberDutyMap.__table__])

def drop_permission():
    db.session.execute(db.text('drop tables if exists position,duty,position_duty_map,member_duty_map'))
    db.session.commit()

def forge_permission():
    member_duty_map=MemberDutyMap(member_id=20221071164,duty='initiate_signin')
    db.session.add(member_duty_map)
    db.session.commit()