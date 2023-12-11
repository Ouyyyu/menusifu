from itertools import zip_longest
import pandas as pd
import json

data_path = '/home/ronghuang/menusifu/data/menu_standard.json'
with open(data_path, 'r') as file:
    data = json.load(file)


combo_names = []  
no_combo_one_price_names=[]
no_combo_two_price_names=[]

s=0

def pro(x):
    if x[0]=='.' or x[0]=='^':
        return x[1:]
    elif '.' in x:
        return x.split('.', 1)[-1]
    elif '(' in x:
        return x.split('(',1)[0]
    return x

if s==0:
    for item in data:
        if 'combo' in data[item]:
            combo_names.append(pro(data[item]['name']))
            
            for x in data[item]['combo']:
                combo_names.append(pro(x['info']['name']))

        else:
            if isinstance(data[item]['price'], dict):
                no_combo_two_price_names.append(pro(data[item]['name']))
            else:
                no_combo_one_price_names.append(pro(data[item]['name']))
else:
    for item in data:
        if 'combo' in data[item]:
            combo_names.append(data[item]['name'])
            
            for x in data[item]['combo']:
                combo_names.append(x['info']['name'])

        else:
            if isinstance(data[item]['price'], dict):
                no_combo_two_price_names.append(data[item]['name'])
            else:
                no_combo_one_price_names.append(data[item]['name'])

# 去除重复项
combo_names = list(set(combo_names))
no_combo_one_price_names=list(set(no_combo_one_price_names))
no_combo_two_price_names=list(set(no_combo_two_price_names))

max_length = max(len(combo_names), len(no_combo_one_price_names), len(no_combo_two_price_names))

combo_names += [''] * (max_length - len(combo_names))
no_combo_one_price_names += [''] * (max_length - len(no_combo_one_price_names))
no_combo_two_price_names += [''] * (max_length - len(no_combo_two_price_names))

df = pd.DataFrame({
    'Combo': combo_names,
    'No combo one price': no_combo_one_price_names,
    'No combo two price': no_combo_two_price_names,
})

# 将数据表保存为 Excel 文件
excel_file_path = f'/home/ronghuang/menusifu/data/menu{s}.xlsx'
df.to_excel(excel_file_path, index=False)

print(f'done to {excel_file_path}')