from wtforms import FileField,SelectField,FieldList,IntegerField
from wtforms import  StringField, validators,BooleanField
from flask_wtf import FlaskForm


class SendMailBase(FlaskForm):
    title = StringField('title', validators=[validators.DataRequired()])
    type = SelectField('type', validators=[validators.DataRequired()])

    receivers_id = FieldList(IntegerField('receiver_id', validators=[validators.NumberRange(min=0)]))
    is_attachment=BooleanField('is_attachment', validators=[validators.DataRequired()])
    attachment=FileField('attachment',validators=[validators.DataRequired(),validators.FileAllowed()])


class SendNotifyMail(SendMailBase):
    body=StringField('body',validators=[validators.DataRequired()])

class SendReplyMail(SendMailBase):
    pass

class SendChoiceMail(SendMailBase):
    pass

class SendJudgeMail(SendMailBase):
    pass
