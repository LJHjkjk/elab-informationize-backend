from elab.db.material import Material
from flask import Blueprint,jsonify,request
from elab.extensions import oidc
from elab.extensions import sqlAlchemy as db

from datetime import datetime
import json
material_manage_blueprint=Blueprint('material',__name__)

# 获取物料信息
@material_manage_blueprint.route('',methods=['GET'])
@oidc.require_login
def get_all_materials():
    # 获取所有的数据
    materials=Material.query.all()
    result=[i.return_to_dict() for i in materials]
    return jsonify({
        'result':'ok',
        'data':result
        })

# 入库
@material_manage_blueprint.route('/checkin',methods=['GET'])
@oidc.require_login
def checkin_materials():
    # 查找需要的物料
    material_id=request.args.get('material_id')
    material=Material.query.get(material_id)

    if not material:
        return jsonify({
            'result':'no',
            'message':'没有这个物料'
            }),400
    
    # 添加
    number=int(request.args.get('number'))
    material.number+=number
    db.session.commit()
    return jsonify({
        'result':'ok',
        'message':'添加成功',
    })

# 出库
@material_manage_blueprint.route('/checkout',methods=['GET'])
@oidc.require_login
def checkout_materials():
    # 查找需要的物料
    material_id=request.args.get('material_id')
    material=Material.query.get(material_id)

    if not material:
        return jsonify({
            'result':'no',
            'message':'没有这个物料'
            }),400
    # 出库
    number=int(request.args.get('number'))
    if number>material.number:
        return jsonify({
            'result':'no',
            'message':'没有这么多库存'
        }),400
    
    material.number-=int(number)
    db.session.commit()
    return jsonify({
        'result':'ok',
        'message':'出库成功',
    })



# 添加新物料
@material_manage_blueprint.route('',methods=['POST'])
@oidc.require_login
def add_materials():
    # 检测权限
    # 检测表单
    form=request.get_json()
    if form==None:
        jsonify({
            'result':'no',
            'message':'请提交正确的格式'
        }),400
    try:
        material=Material(
            name=form.get('name'),
            price=form.get('price'),
            number=form.get('number'),
            security_value=form.get('security_value'),
            source=form.get('source'),
            type=form.get('type'),
            bar_code=form.get('bar_code'),
            position=form.get('position'),
            remark=form.get('remark'),
            warehousing_date=datetime.strptime(form.get('warehousing_date'), "%Y-%m-%d").date()
             if 'warehousing_date' in form else None, 
            state=form.get('state'),
        )
        db.session.add(material)
        db.session.commit()
        return jsonify({
            'result':'ok',
            'message':'添加成功',
        })

    except Exception as e:
        return jsonify({
            'result':'no',
            'message':e,
        }),400



# 删除物料
@material_manage_blueprint.route('',methods=['DELETE'])
@oidc.require_login
def delete_materials():
    # 检测权限
    material_id=request.get_json()['id']
    material=Material.query.get(material_id)

    if material==None:
        return jsonify({
            'result':'no',
            'message':'没有这个物料'
            }),400
    db.session.delete(material)
    db.session.commit()
    return jsonify({
        'result':'ok',
        'message':'删除成功',
    })
    
    

# 修改物料
@material_manage_blueprint.route('',methods=['PUT'])
@oidc.require_login
def modify_materials():
    # 检测权限
    # 检测表单
    form=request.get_json()
    if form==None:
        jsonify({
            'result':'no',
            'message':'请提交正确的格式'
        }),400
    
    material=Material.query.get(form.get('id'))
    if not material:
        return jsonify({
            'result':'no',
            'message':'没有这个物料',
        }),400

    try:
        material
        material.name=form.get('name'),
        material.price=form.get('price'),
        material.number=form.get('number'),
        material.security_value=form.get('security_value'),
        material.source=form.get('source'),
        material.type=form.get('type'),
        material.bar_code=form.get('bar_code'),
        material.position=form.get('position'),
        material.remark=form.get('remark'),
        material.warehousing_date=datetime.strptime(form.get('warehousing_date'), "%Y-%m-%d").date()\
            if 'warehousing_date' in form else None, 
        material.state=form.get('state'),

        db.session.commit()
        return jsonify({
            'result':'ok',
            'message':'修改成功',
        })

    except Exception as e:
        return jsonify({
            'result':'no',
            'message':e,
        }),400


def material_manage_init(service_blueprint):
    service_blueprint.register_blueprint(material_manage_blueprint,url_prefix='/material')