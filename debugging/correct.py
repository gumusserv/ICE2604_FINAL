import json

with open('./static/graph_tag.json','r',encoding='utf-8') as f:
    graph_dic = json.load(f)



new_dic = {}

for i in range(len(graph_dic['nodes'])):
    graph_dic['nodes'][i]['id'] = i
    new_dic[graph_dic['nodes'][i]['label']] = i

for i in range(len(graph_dic['edges'])):
    sourceID  = graph_dic['edges'][i]['sourceID']
    targetID  = graph_dic['edges'][i]['targetID']
    sourceID = new_dic[sourceID]
    targetID = new_dic[targetID]
    graph_dic['edges'][i]['sourceID'] = sourceID
    graph_dic['edges'][i]['targetID'] = targetID



with open('./static/graph_tag.json','w',encoding='utf-8') as f:
    json.dump(graph_dic,fp = f,indent = 2,sort_keys= True,ensure_ascii = False)