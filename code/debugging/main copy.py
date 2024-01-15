from flask import Flask,request,render_template,redirect,url_for
import pymysql
import json
import random
from query import simple_serach,select_random,select_author

app = Flask(__name__)

@app.route('/',methods = ['GET'])
def home():
    return render_template('home.html')

@app.route('/data', methods=['GET'])
def get_data():
    data = {}
    data["random_varse"] = select_random()
    return json.dumps(data)

@app.route('/author/',methods = ['GET'])
def poet_all():
    
    return redirect("/author/dynasty=不限/page=1")

@app.route('/author/dynasty=<dyn>/page=<page>',methods = ['GET'])
def poet_all_dynasty(dyn,page):
    # conn = pymysql.Connect(host = '127.0.0.1',port = 3306,user = 'root',password = 'root',db = 'chinesepoetry',charset='utf8mb4')
    # cursor = conn.cursor()
    # if dyn == '不限':
    #     dyn = '唐代'
    #     cursor.execute(''' select name,brief_intro,poem_sum,id,avatar_link from poet where dynasty = %s ''','唐代')
    # else:
    #     cursor.execute(''' select name,brief_intro,poem_sum,id,avatar_link from poet where dynasty = %s ''',dyn)
    # poet_tuple = cursor.fetchall()
    # length = len(poet_tuple)
    # all_pages = (length - 1) // 10 + 1
    # page = int(page)
    # if page == all_pages:
    #     poet_tuple = poet_tuple[(page - 1) * 10:]
    # elif page < all_pages and page > 0:
    #     poet_tuple = poet_tuple[(page - 1) * 10 :page * 10 ]
    # else:
    #     poet_tuple = poet_tuple[0:10]
    poet_tuple = select_author(dyn,page)
     
    
    
    
    return render_template('poet_all_new.html',dynasty = dyn,data = poet_tuple,page = int(page))

@app.route('/poetry/',methods = ['GET'])
def poetry_all():
    return redirect("/poetry/dynasty=不限/page=1")

@app.route('/poetry/dynasty=<dyn>/page=<page>',methods = ['GET'])
def poetry_all_dynasty(dyn,page):
    conn = pymysql.Connect(host = '127.0.0.1',port = 3306,user = 'root',password = 'root',db = 'chinesepoetry',charset='utf8mb4')
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
    
    return render_template('poetry_all.html',dynasty = dyn,page = page,data = poetry_tuple,\
                                            tag_list = tag_list,length = length,type_list = type_list)


@app.route('/poetry/poetryId=<poetryId>',methods = ['GET'])
def poetry_detail(poetryId):
    conn = pymysql.Connect(host = '127.0.0.1',port = 3306,user = 'root',password = 'root',db = 'chinesepoetry',charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(''' select authorid,author,dynasty,tags,content,fanyi,shangxi,name from poem where id = %s ''',poetryId)
    poetry = cursor.fetchone()
    cursor.execute(''' select brief_intro from poet where id = %s ''',poetry[0])
    intro_poet = cursor.fetchone()[0]

    return render_template('poetry_detail.html',title = poetry[7],tags = json.loads(poetry[3]),intro_poet = intro_poet,\
                                                fanyi = json.loads(poetry[5]),content = json.loads(poetry[4]),\
                                                shangxi = json.loads(poetry[6]),author = poetry[1])

@app.route('/author/poetid=<poetid>')
def poet(poetid):
    print(poetid)
    conn = pymysql.Connect(host = '127.0.0.1',port = 3306,user = 'root',password = 'root',db = 'chinesepoetry',charset='utf8mb4')
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

    return render_template('poet_detail.html',name = name,intro = intro,sum = sum,detail_info = detail_info,poetid = poetid,img = img)


@app.route("/data2/<name>",methods = ['GET'])
def get_data2(name):
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
    

    data_list = []

    length = len(ans_dic['style'])

    for i in range(length):
        data_dic = {}
        data_dic['value'] = ans_dic['sum'][i]
        data_dic['name'] = ans_dic['style'][i]
        data_list.append(data_dic)
    
    final_dic = {}
    final_dic['data'] = data_list
    return json.dumps(final_dic)


@app.route('/poetry/poetid=<poetid>/page=<page>',methods = ['GET'])
def poetry_of_poet(poetid,page):
    conn = pymysql.Connect(host = '127.0.0.1',port = 3306,user = 'root',password = 'root',db = 'chinesepoetry',charset='utf8mb4')
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

    return render_template('poetry_of_poet.html',dynasty = dyn,page = page,poetid = poetid,type_list = type_list,\
                            poet = author,data = poetry_tuple,tag_list = tag_list,length = length)


@app.route('/poetry/type=<typ>/page=<page>',methods = ['GET'])
def poetry_all_type(typ,page):
    print(typ)
    type_tmp = []
    type_list = []
    with open('./tag_dic.json',encoding='utf-8') as f:
        type_dic = json.load(fp = f)
    for i in type_dic:
        type_tmp.append(i)
    random_list = random.sample(range(0,100),10)
    for random_num in random_list:
        type_list.append(type_tmp[random_num])

    conn = pymysql.Connect(host = '127.0.0.1',port = 3306,user = 'root',password = 'root',db = 'chinesepoetry',charset='utf8mb4')
    cursor = conn.cursor()
    
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

    
    return render_template('poetry_all_type.html',type = typ,type_list = type_list,page = page,data = poetry_tuple,\
                            tag_list = tag_list,length = length,dynasty_list = dynasty_list     )
                              
@app.route('/varses/page=<page>',methods = ['GET'])
def varses(page):
    random_list = random.sample(range(1,27557),10)
    

    conn = pymysql.Connect(host = '127.0.0.1',port = 3306,user = 'root',password = 'root',db = 'chinesepoetry',charset='utf8mb4')
    cursor = conn.cursor()
    
    varses_list = []
    for i in random_list:
        cursor.execute(''' select varses,source from famous_varses where id = {}'''.format(i))
        varse = cursor.fetchone()
        varses_list.append(varse)
    

    page = int(page)

    return render_template('varses.html',varses_list = varses_list,page = page)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5000,debug = True)