from .index import open_file
from elab.db.material import Material,db
import os
# 从表格中导入物料信息
def import_material_info(path):
    df=open_file(path)
    new_materials=[]
    df.fillna('', inplace=True)
    # 添加物料
    for index,row in df.iterrows():
        if row['name']=='':
            continue
        new_material=Material(
            name=row['name'],
            source='现有',
            type=row['type'],
            position=row['place'],
            remark=row['remark']
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