from elab.db import sqlAlchemy as db
from faker import Faker


class Material(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    price=db.Column(db.Integer)
    number=db.Column(db.Integer)
    security_value=db.Column(db.Integer)
    source=db.Column(db.String(100))
    type=db.Column(db.String(100))
    bar_code=db.Column(db.String(100))
    position=db.Column(db.String(100))
    remark=db.Column(db.String(500))
    warehousing_date=db.Column(db.String(100))
    state=db.Column(db.String(100))

    def return_to_dict(self):
        result={
            'id':self.id,
            'name':self.name,
            'price':self.price,
            'number':self.number,
            'security_value':self.security_value,
            'source':self.source,
            'type':self.type,
            'bar_code':self.bar_code,
            'position':self.position,
            'remark':self.remark,
            'warehousing_date':self.warehousing_date,
            'state':self.state,
        }
        return result
        

def init_material():
    db.metadata.create_all(bind=db.engine, tables=[Material.__table__])


def drop_material():
    try:
        db.session.execute(db.text('drop table if exists material'))
        db.session.commit()
    except Exception as e:
        print(e)


def forge_material():
    fake=Faker('zh_CN')
    
    # 添加200种物料
    for i in range(0,200):
        material=Material(
            name=fake.word(),
            price=fake.random_int(),
            number=fake.random_int(min=0),
            security_value=0,
            source=fake.company(),
            type=fake.word(),
            bar_code=fake.uuid4(),
            position=fake.word(),
            remark=fake.sentence(),
            warehousing_date=fake.date_this_decade(),
            state=fake.word(),
        )
        db.session.add(material)
        db.session.commit()
    
