with open('./static/graph_tag.json','w',encoding='utf-8') as f:
    json.dump(graph_dic,fp = f,indent = 2,sort_keys= True,ensure_ascii = False)