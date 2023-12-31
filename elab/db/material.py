from elab.db import sqlAlchemy as db
from faker import Faker
from datetime import datetime

class Material(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    # 名称
    name=db.Column(db.String(100),nullable=False)
    # 价格
    price=db.Column(db.Integer)
    # 目前数量
    number=db.Column(db.Integer)
    # 安全值
    security_value=db.Column(db.Integer)
    # 来源
    source=db.Column(db.String(100))
    # 类型
    type=db.Column(db.String(100))
    # 条形码
    bar_code=db.Column(db.String(100))
    # 位置
    position=db.Column(db.String(100))
    # 备注
    remark=db.Column(db.Text)
    # 入库日期
    warehousing_date=db.Column(db.String(100),default=datetime.now())
    # 状态
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

    def generate_unique_words(count):
        unique_words = set()

        while len(unique_words) < count:
            random_word = fake.word()
            unique_words.add(random_word)

        return list(unique_words)
    unique_words_list = generate_unique_words(200)
    

    # 添加200种物料
    for i in range(0,200):
        material=Material(
            name=unique_words_list[i],
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
    
