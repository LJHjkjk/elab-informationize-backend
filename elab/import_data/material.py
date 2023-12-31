from .index import open_file
from elab.db.material import Material,db
import os
# 从表格中导入物料信息
def import_material_info(path):
    df=open_file(path)
    new_materials=[]
    # 添加物料
    for index,row in df.iterrows():
        if row['名称（不认识的用淘宝识图）'] is None and row['PLACE'] is None:
            break
        if row['名称（不认识的用淘宝识图）'] is None:
            continue
        print(row)
        new_material=Material(
            name=row['名称（不认识的用淘宝识图）'],
            source='现有',
            type=row[' 名称/储物类别'],
            position=row['PLACE'],
            remark=row['备注(自行添加)']
        )
        new_materials.append(new_material)
    db.session.add_all(new_materials)
    db.session.commit()
    

def import_material_info_from_directory(directory_path):
    print(os.listdir(directory_path))
    file_list = os.listdir(directory_path)
    for i in file_list:
        try:
            import_material_info(os.path.join(directory_path, i))
            print(i+'导入成功')
        except Exception as error:
            print(i+"发生错误   ",error)