import pymysql
import json

name_list = ['屈原','李白','杜甫','白居易','苏轼','陶渊明','王维','李商隐','李煜','辛弃疾']
with open('./static/graph_tag.json','r',encoding='utf-8') as f:
    dic_pragh = json.load(f)
tmp_list = dic_pragh['nodes']
tag_list = []
for i in range(0,24):
    tag_list.append(tmp_list[i]['id'])
data_list1 = []
print(tag_list)
j = 0
for name in name_list:
    conn = pymysql.connect( host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='chinesepoetry',
                        charset="utf8")

    cursor = conn.cursor()
    cursor.execute(''' select style from poets_table where poet = %s ''',name)
    style = cursor.fetchone()
    style = style[0]
    style = style.split('/')
    style_list = []
    sum_list = []


    style_dic = {}
    for one in style:
        index = one.find(':')
        if index == -1:
            break
        style_dic[one[0:index]] = int(one[index + 1:])
        
    style_dic = sorted(style_dic.items(),key = lambda x:x[1],reverse = True)
    if len(style_dic) > 10:
        style_dic = style_dic[0:10]
    for one in style_dic:
        style_list.append(one[0])
        sum_list.append(one[1])
    ans_dic = {}
    ans_dic['style'] = style_list
    ans_dic['sum'] = sum_list


    data_list = []

    length = len(ans_dic['style'])

    for i in range(length):
        data_dic = {}
        data_dic['value'] = ans_dic['sum'][i]
        data_dic['name'] = ans_dic['style'][i]
        data_list.append(data_dic)

    final_dic = {}
    for data in data_list:
        final_dic[data['name']] = data['value']

    for k in range(24):
        if tag_list[k] in final_dic:
            data_list1.append([j,k,final_dic[tag_list[k]]])
        else:
            data_list1.append([j,k,0])

    j += 1


print(data_list1)