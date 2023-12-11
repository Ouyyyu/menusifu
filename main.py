import pandas as pd
import json

data_path='/home/ronghuang/menusifu/data/cases.json'
menu_path='/home/ronghuang/menusifu/data/menu0.xlsx'

menu = pd.read_excel(menu_path)

data_path='/home/ronghuang/menusifu/data/10_20_helen_text_test_checked.json'

with open(data_path, 'r') as file:
    data = json.load(file)

def con(dish,price_type,ca):
    t=''
    
    if price_type==ca:
        t='this is true'

    else:
        if len(price_type)==1: 
            if price_type[0]!='No combo two price':
                t=f'{dish}, anything else?'

            else:
                t=t=f'for {dish}, what size would you like? small, or large?'

        elif len(price_type)==2:#肯定有combo
            if price_type[1]=='No combo two price':
                t=f'for {dish}, what size would you like? small, large or combination?'

            else:
                t=f'for {dish}, what size would you like? with combination or not?'
        
        else:
            t='error'

    return f'**agent:{t}'

def process(a,x):#a：x的前一句话  a 是顾客说的  x 机器人
    global menu
    a=a.split(':',1)[-1]
    x=x.split(':', 1)[-1]

    dishes=[]
    price_type=[]
    dish=''

    for column in menu.columns:
        for value in menu[column]:
            if pd.notnull(value):  # 检查值是否不是 NaN
                if value.lower() in x:
                    dishes.append(value.lower())
            else:
                break
        

    dishes=list(set(dishes))#备选菜单

    if dishes:
        #确定唯一菜
        dish = max(dishes, key=lambda ca: (x.find(ca) + len(ca), len(ca)))

    
    if dish and dish in a:#判断是否新菜 并且找出这个菜拥有的价格类型
        for column in menu.columns:
            if menu[column].apply(lambda x: dish in str(x).lower()).any():
                price_type.append(column)

        ca=[]# x中存在的价格类型
        if 'size' in x:
            if 'combination' in x:
                ca.append('Combo')

            if 'small' in x and 'large' in x:
                ca.append('No combo two price')

        elif len(price_type)==1 and price_type[0]!='No combo two price':
            ca.append(price_type[0])

        print(a)
        print(x)
        print(dish)
        print(price_type,ca,'\n')

        return dish+' '+str(price_type)+' '+con(dish,price_type,ca)        
        
    return ''

dict={}
for item in data:
    print(item[0])
    re_list=[]
    a=''

    for x in item[1]:
        re_list.append(x)
        if isinstance(x,str) and 'agent' in x:
            t=process(a,x)
            if t:
                re_list.append(t)
        
        if isinstance(x,str) and 'customer' in x:
            a=x
    
    dict[item[0]]=re_list

# 将字典保存为 JSON 文件
save_path = '/home/ronghuang/menusifu/result/10_20_helen_text_test_checked_result.json'
with open(save_path, 'w') as outfile:
    json.dump(dict, outfile, indent=2)  # 使用 json.dump() 将字典保存为 JSON 文件

print(f'Data saved to {save_path}')