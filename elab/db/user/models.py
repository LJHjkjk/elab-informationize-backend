from user import db




class UserInfo(db.Model):
    id=db.Column(db.Integer,db.ForeignKey('user.name'),primary_key=True)



