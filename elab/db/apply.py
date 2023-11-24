from elab.db import sqlAlchemy as db


# 申请的基类
class Apply(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    applicant_id=db.Column(db.Integer)
    applicant_name=db.Column(db.String)
    application_datetime=db.Column(db.DateTime)
    handler_id=db.Column(db.Integer)
    handler_name=db.Column(db.String)
    handler_datetime=db.Column(db.DateTime)
    finished_state=db.Column(db.Boolean)

    # 虚函数
    # 一个申请处理完成之后调用这个
    def after_handle():
        print(1)


# 科研助手申请
class ResearchAssistantApply(Apply):
    is_file=db.Column(db.Boolean)
    # 结合具体的文件系统
    file=db.Column(db.Integer)
    # 记录申请结果


    def after_handle():
        pass


# 报销申请
class ReimbursementApply(Apply):
    # 申请
    content=db.Column(db.String(100))
    price=db.Column(db.Float)
    cause=db.Column(db.Text)
    # 完成情况
    finished_state=db.Column(db.Enum(1,2,3))
    # 上传发票
    upload_invoice_datetime=db.Column(db.DateTime)
    is_upload_invoice=db.Column(db.Boolean)
    invoice=db.Column(db.String(100))
    # 接受发票者
