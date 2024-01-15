import pymysql
from itertools import chain
import random
import json



sql = 'SELECT varses FROM famous_varses WHERE varses LIKE %s'
sql_random = 'SELECT varses,source FROM famous_varses WHERE id = %s'

def simple_serach(keyword):
    conn = pymysql.connect( host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='chinesepoetry',
                        charset="utf8")

    cursor = conn.cursor()
    cursor.execute(sql, "%"+keyword+"%")
    result=cursor.fetchall()
    resultlist = list(chain.from_iterable(result))
    return resultlist

def select_random():
    conn = pymysql.connect( host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='chinesepoetry',
                        charset="utf8")

    cursor = conn.cursor()
    id=random.randrange(1,27557)
    cursor.execute(sql_random, str(id))
    result=cursor.fetchone()
    return result

def select_author(dyn,page):
    conn = pymysql.connect( host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='chinesepoetry',
                        charset="utf8")

    cursor = conn.cursor()
    if dyn == '不限':
        dyn = '唐代'
        cursor.execute(''' select name,brief_intro,poem_sum,id,avatar_link from poet where dynasty = %s ''','唐代')
    else:
        cursor.execute(''' select name,brief_intro,poem_sum,id,avatar_link from poet where dynasty = %s ''',dyn)
    poet_tuple = cursor.fetchall()
    length = len(poet_tuple)
    all_pages = (length - 1) // 10 + 1
    page = int(page)
    if page == all_pages:
        poet_tuple = poet_tuple[(page - 1) * 10:]
    elif page < all_pages and page > 0:
        poet_tuple = poet_tuple[(page - 1) * 10 :page * 10 ]
    else:
        poet_tuple = poet_tuple[0:10]

    return poet_tuple


def select_poetry(dyn,page):
    conn = pymysql.connect( host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='chinesepoetry',
                        charset="utf8")

    cursor = conn.cursor()
    if dyn == '不限':
        cursor.execute(''' select name,authorid,tags,final_score,content,id,author from poem \
                           where dynasty = '唐代' order by final_score DESC''')
    else:
        cursor.execute(''' select name,authorid,tags,final_score,content,id,author from poem \
                           where dynasty = %s order by final_score DESC''',dyn)

    poetry_tuple = cursor.fetchall()


    length = len(poetry_tuple)
    all_pages = (length - 1) // 10 + 1
    page = int(page)
    if page == all_pages:
        poetry_tuple = poetry_tuple[(page - 1) * 10:]
    elif page < all_pages and page > 0:
        poetry_tuple = poetry_tuple[(page - 1) * 10 :page * 10 ]
    else:
        poetry_tuple = poetry_tuple[0:10]
    

    length = len(poetry_tuple)
    tag_list = []
    

    for poetry in poetry_tuple:
        if(poetry[2] != '"None"'):
            tag_list.append(json.loads(poetry[2]))
        else:
            tag_list.append([])



    poetry_tuple = list(poetry_tuple)
    
    for i in range(len(poetry_tuple)):
        poetry_tuple[i] = list(poetry_tuple[i])
        poetry_tuple[i][2] = json.loads(poetry_tuple[i][2])
        poetry_tuple[i][4] = json.loads(poetry_tuple[i][4])
    
        sentence_list = poetry_tuple[i][4]
        for j in range(len(sentence_list)):
            str_tmp = sentence_list[j].replace('\n','')
            str_tmp = str_tmp.replace('\r','')
            sentence_list[j] = str_tmp
        poetry_tuple[i][4] = sentence_list
    
    type_tmp = []
    type_list = []
    with open('./tag_dic.json',encoding='utf-8') as f:
        type_dic = json.load(fp = f)
    for type in type_dic:
        type_tmp.append(type)
    random_list = random.sample(range(0,100),10)
    for random_num in random_list:
        type_list.append(type_tmp[random_num])

    data_list = [poetry_tuple, tag_list, length, type_list]
    return data_list



def select_poetryId(poetryId):
    conn = pymysql.connect( host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='chinesepoetry',
                        charset="utf8")

    cursor = conn.cursor()
    cursor.execute(''' select authorid,author,dynasty,tags,content,fanyi,shangxi,name from poem where id = %s ''',poetryId)
    poetry = cursor.fetchone()
    cursor.execute(''' select brief_intro from poet where id = %s ''',poetry[0])
    intro_poet = cursor.fetchone()[0]
    return [poetry,intro_poet]

def select_poetid(poetid):
    conn = pymysql.connect( host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='chinesepoetry',
                        charset="utf8")

    cursor = conn.cursor()
    cursor.execute("select brief_intro from poet where id = %s",poetid)
    a = cursor.fetchone()
    intro = a[0]
    cursor.execute("select poem_sum from poet where id = %s",poetid)
    a = cursor.fetchone()
    sum = a[0]
    cursor.execute('select detail_info from poet where id = %s',poetid)
    a = cursor.fetchone()
    detail_info = json.loads(a[0])
    cursor.execute("select name from poet where id = %s",poetid)
    a = cursor.fetchone()
    name = a[0]
    cursor.execute("select avatar_link from poet where id = %s",poetid)
    a = cursor.fetchone()
    img = a[0]
    return [name, intro, sum, detail_info,img]

def get_graph_data(name):
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
    final_dic['data'] = data_list

    return final_dic
def get_graph_data1(name):
    conn = pymysql.Connect(host = '127.0.0.1',port = 3306,user = 'root',password = 'root',db = 'chinesepoetry',charset='utf8mb4')
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
    return ans_dic

def select_poemofPoet(poetid,page):
    conn = pymysql.connect( host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='chinesepoetry',
                        charset="utf8")

    cursor = conn.cursor()
    cursor.execute(''' select name,tags,content,id from \
                        poem where authorid = %s ''',poetid)
    
    
    poetry_tuple = cursor.fetchall()

    cursor.execute(''' select dynasty from poet where id = %s ''',poetid)
    dyn = cursor.fetchone()

    cursor.execute(''' select name from poet where id = %s ''',poetid)
    author = cursor.fetchone()


    length = len(poetry_tuple)
    all_pages = (length - 1) // 10 + 1
    page = int(page)
    if page == all_pages:
        poetry_tuple = poetry_tuple[(page - 1) * 10:]
    elif page < all_pages and page > 0:
        poetry_tuple = poetry_tuple[(page - 1) * 10 :page * 10 ]
    else:
        poetry_tuple = poetry_tuple[0:10]
    
    length = len(poetry_tuple)
    tag_list = []
    

    for poetry in poetry_tuple:
        if(poetry[1] != '"None"'):
            tag_list.append(json.loads(poetry[1]))
        else:
            tag_list.append([])

    poetry_tuple = list(poetry_tuple)
    
    for i in range(len(poetry_tuple)):
        poetry_tuple[i] = list(poetry_tuple[i])
        poetry_tuple[i][1] = json.loads(poetry_tuple[i][1])
        poetry_tuple[i][2] = json.loads(poetry_tuple[i][2])
    
        sentence_list = poetry_tuple[i][2]
        for j in range(len(sentence_list)):
            str_tmp = sentence_list[j].replace('\n','')
            str_tmp = str_tmp.replace('\r','')
            sentence_list[j] = str_tmp
        poetry_tuple[i][2] = sentence_list
    
    type_tmp = []
    type_list = []
    with open('./tag_dic.json',encoding='utf-8') as f:
        type_dic = json.load(fp = f)
    for i in type_dic:
        type_tmp.append(i)
    random_list = random.sample(range(0,100),10)
    for random_num in random_list:
        type_list.append(type_tmp[random_num])
    return [dyn, type_list, author, poetry_tuple, tag_list, length]

def select_type(typ,page):
    conn = pymysql.connect( host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='chinesepoetry',
                        charset="utf8")

    cursor = conn.cursor()
    type_tmp = []
    type_list = []
    with open('./tag_dic.json',encoding='utf-8') as f:
        type_dic = json.load(fp = f)
    for i in type_dic:
        type_tmp.append(i)
    random_list = random.sample(range(0,100),10)
    for random_num in random_list:
        type_list.append(type_tmp[random_num])

   
    
    cursor.execute(''' select name,authorid,tags,final_score,content,id,author,dynasty from poem \
                       where tags like '%{}%' order by final_score DESC'''.format(typ))

    poetry_tuple = cursor.fetchall()



    length = len(poetry_tuple)
    all_pages = (length - 1) // 10 + 1
    page = int(page)
    if page == all_pages:
        poetry_tuple = poetry_tuple[(page - 1) * 10:]
    elif page < all_pages and page > 0:
        poetry_tuple = poetry_tuple[(page - 1) * 10 :page * 10 ]
    else:
        poetry_tuple = poetry_tuple[0:10]
    
    length = len(poetry_tuple)

    tag_list = []
    dynasty_list = []
    for poetry in poetry_tuple:
        if(poetry[2] != '"None"'):
            tag_list.append(json.loads(poetry[2]))
        else:
            tag_list.append([])
        dynasty_list.append(poetry[7])

    poetry_tuple = list(poetry_tuple)
    
    for i in range(len(poetry_tuple)):
        poetry_tuple[i] = list(poetry_tuple[i])
        poetry_tuple[i][2] = json.loads(poetry_tuple[i][2])
        poetry_tuple[i][4] = json.loads(poetry_tuple[i][4])
    
        sentence_list = poetry_tuple[i][4]
        for j in range(len(sentence_list)):
            str_tmp = sentence_list[j].replace('\n','')
            str_tmp = str_tmp.replace('\r','')
            sentence_list[j] = str_tmp
        poetry_tuple[i][4] = sentence_list
    return [type_list, poetry_tuple, tag_list, length, dynasty_list]

def select_varses(page):
    conn = pymysql.connect( host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='chinesepoetry',
                        charset="utf8")

    cursor = conn.cursor()
    random_list = random.sample(range(1,27557),10)
    
    varses_list = []
    for i in random_list:
        cursor.execute(''' select varses,source from famous_varses where id = {}'''.format(i))
        varse = cursor.fetchone()
        varses_list.append(varse)
    

    
    return varses_list


def search_poet(keyword,page):
    conn = pymysql.connect( host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='chinesepoetry',
                        charset="utf8")

    cursor = conn.cursor()
    cursor.execute(''' select id,name,dynasty,brief_intro,avatar_link from poet where name like '%{}%' \
                        order by score DESC'''.format(keyword))

    a = cursor.fetchall()
    length = len(a)
    all_pages = (length - 1) // 10 + 1
    page = int(page)
    if page == all_pages:
        a = a[(page - 1) * 10:]
    elif page < all_pages and page > 0:
        a = a[(page - 1) * 10 :page * 10 ]
    else:
        a = a[0:10]
    
    length = len(a)
    return a
