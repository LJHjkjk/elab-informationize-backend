import pandas as pd
import os

def open_file(path):
        # 获取文件类型
    _, file_extension = os.path.splitext(path)
    file_extension = file_extension.lower()
    # 读取文件
    if file_extension=='.csv':
        df = pd.read_csv(path)
    elif file_extension=='.xlsx':
        df = pd.read_excel(path)
    else:
        raise Exception('不支持类型'+file_extension)
    
    return df