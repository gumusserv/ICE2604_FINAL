import json
import pymysql
import random
import math
# with open('./connect_grapg.json','r',encoding='utf-8') as f:
#     dic = json.load(f)

# # node_list = dic['nodes']
# # i = 0
# # s = set()
# # for node in node_list:
    
# #     i += 1
# #     s.add(node['label'])
# #     if node['label'] == 'twitter':
# #         print(node['label'])
# # print(i)
# # print(len(s))



# edge_list = dic['edges']
# for edge in edge_list:
#     print(edge['size'])

def random_color():
    colors1 = '0123456789ABCDEF'
    num = "#"
    for i in range(6):
        num += random.choice(colors1)
    return num

radius = 1000

if __name__ == '__main__':
    conn = pymysql.connect( host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='chinesepoetry',
                        charset="utf8")

    cursor = conn.cursor()
    sql = ''' select tags from poem where tags != 'None' '''
    cursor.execute(sql)
    tag_tuple = cursor.fetchall()
    nodes_dic = {}
    for tag in tag_tuple:
        tag_list = json.loads(tag[0])
        for one in tag_list:
            if one not in nodes_dic:
                nodes_dic[one] = 1
            else:
                nodes_dic[one] += 1
    # with open('./nodes.json','w',encoding='utf-8') as f:
    #     json.dump(nodes_dic,fp = f,indent = 2,sort_keys= True,ensure_ascii = False)

    final_dic = {}

    sql = ''' select tags from poem where tags != 'None' '''
    cursor.execute(sql)
    tag_tuple = cursor.fetchall()
    nodes_dic = {}
    for tag in tag_tuple:
        tag_list = json.loads(tag[0])
        for one in tag_list:
            if one not in nodes_dic:
                nodes_dic[one] = 1
            else:
                nodes_dic[one] += 1
    nodes_list = sorted(nodes_dic.items(),key = lambda x:x[1],reverse = True)
    list1 = []
    sum_node = len(nodes_list)
    node_size_min = 1
    node_size_max = 10202
    node_size_medium = 2063
    for i in range(sum_node):
        tmp_dic = {}
        while True:
            x = random.uniform(-radius, radius)
            y = random.uniform(-radius, radius)
            if (x ** 2) + (y ** 2) <= (radius ** 2):
                
                break

        
        tmp_dic['color'] = random_color()
        tmp_dic['attributes'] = {}
        tmp_dic['y'] = y
        tmp_dic['x'] = x
        tmp_dic['label'] = nodes_list[i][0]
        tmp_dic['id'] = nodes_list[i][0]
        if i < 10:
            tmp_dic['size'] = (nodes_list[i][1] - node_size_medium) / (node_size_max - node_size_medium) * 50 + 50
        else:
            tmp_dic['size'] = (nodes_list[i][1] - node_size_min) / (node_size_medium - node_size_min) * 20
        list1.append(tmp_dic)

    final_dic['nodes'] = list1

    
    
    sql = ''' select tags from poem where tags != 'None' '''
    cursor.execute(sql)
    tag_tuple = cursor.fetchall()
    edges_dic = {}
    for tag in tag_tuple:
        tag_list = json.loads(tag[0])
        for i in range(len(tag_list)):
            for j in range(i + 1,len(tag_list)):
                key = (tag_list[i],tag_list[j])
                if key not in edges_dic:
                    edges_dic[key] = 1
                else:
                    edges_dic[key] += 1
    edges_list = sorted(edges_dic.items(),key = lambda x:x[1],reverse = True)
    list2 = []
    edges_sum = int(942 / 717 * sum_node / 2)
    print(edges_sum)
    for edge in edges_list[0:edges_sum]:
        tmp_dic = {}
        sourceID = edge[0][0]
        targetID = edge[0][1]
        size = edge[1]
        

        tmp_dic['sourceID'] = sourceID
        tmp_dic['targetID'] = targetID
        tmp_dic['attributes'] = {}
        tmp_dic['size'] = math.log(size)
        list2.append(tmp_dic)

    
    final_dic['edges'] = list2


    
    with open('./static/graph_tag.json','w',encoding='utf-8') as f:
        json.dump(final_dic,fp = f,indent = 2,sort_keys= True,ensure_ascii = False)

    
    