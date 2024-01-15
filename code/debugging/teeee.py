import json

with open('./connect_grapg.json','r',encoding='utf-8') as f:
    dic = json.load(f)

print(len(dic['nodes']))
print(len(dic['edges']))