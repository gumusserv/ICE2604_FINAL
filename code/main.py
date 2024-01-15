from flask import Flask,request,render_template,redirect,url_for
import pymysql
import json
import random
from query import simple_serach,select_random,select_author,\
                    select_poetry,select_poetryId,select_poetid,get_graph_data,\
                    select_poemofPoet,select_type,select_varses,search_poet,get_graph_data1
from search import es_search

import tensorflow as tf
from dataset import tokenizer
import settings
import utils


model = tf.keras.models.load_model(settings.BEST_MODEL_PATH)
sentences = utils.generate_random_poetry(tokenizer, model).replace('。','。\n').split('。')

app = Flask(__name__)

@app.route('/',methods = ['GET'])
def home():
    return render_template('home.html')

@app.route('/graph/data',methods = ['GET'])
def graph():
    return render_template('graph_data.html')

@app.route('/graph/tag1',methods = ['GET'])
def graph_tag1():
    return render_template('graph_tag1.html')

@app.route('/graph/tag2',methods = ['GET'])
def graph_tag2():
    return render_template('graph_tag2.html')

@app.route('/graph/china',methods = ['GET'])
def graph_china():
    return render_template('graph_china.html')

@app.route('/graph/reli',methods = ['GET'])
def graph_reli():
    return render_template('graph_reli.html')

@app.route('/AIPoetry',methods = ['GET'])
def AI():
    
    sentence1 = sentences[0]
    sentence2 = sentences[1]
    return render_template('AI.html',sentence1 = sentence1,sentence2 = sentence2)

@app.route('/AIPoetry/header',methods = ['GET'])
def AI_header():
    keyword = request.args.get('keyword')
    sentences = utils.generate_acrostic(tokenizer, model, head=keyword).replace('。','。\n').split('。')
    sentence1 = sentences[0]
    sentence2 = sentences[1]
    return render_template('AI_header.html',sentence1 = sentence1,sentence2 = sentence2,keyword = keyword)

@app.route('/AIPoetry/complete',methods = ['GET'])
def AI_complete():
    keyword = request.args.get('keyword')
    sentences = utils.generate_random_poetry(tokenizer, model, s = keyword).replace('。','。\n').split('。')
    sentence1 = sentences[0]
    sentence2 = sentences[1]
    return render_template('AI_complete.html',sentence1 = sentence1,sentence2 = sentence2,keyword = keyword)

@app.route('/data', methods=['GET'])
def get_data():
    data = {}
    data["random_varse"] = select_random()
    return json.dumps(data)

@app.route('/AIdata', methods=['GET'])
def get_AIdata():
    sentences = utils.generate_random_poetry(tokenizer, model).replace('。','。\n').split('。')
    data = {}
    data["sentence1"] = sentences[0] + '。'
    data["sentence2"] = sentences[1] + '。'
    return json.dumps(data)

@app.route('/AIdata/header/keyword=<keyword>', methods=['GET'])
def get_AIdata_header(keyword):
    sentences = utils.generate_acrostic(tokenizer, model, head=keyword).replace('。','。\n').split('。')
    data = {}
    data["sentence1"] = sentences[0] + '。'
    data["sentence2"] = sentences[1] + '。'
    return json.dumps(data)

@app.route('/AIdata/complete/keyword=<keyword>', methods=['GET'])
def get_AIdata_complete(keyword):
    sentences = utils.generate_random_poetry(tokenizer, model, s = keyword).replace('。','。\n').split('。')
    data = {}
    data["sentence1"] = sentences[0] + '。'
    data["sentence2"] = sentences[1] + '。'
    return json.dumps(data)

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == "POST":
        keyword = request.form['keyword']
        poems = simple_serach(keyword)
        return redirect(url_for('result',  keyword=keyword, poems=poems))
    return render_template("search.html")

@app.route('/result/page=1', methods=['GET'])
def result():
    keyword = request.args.get('keyword')
    poems = es_search(keyword)
    return render_template("result.html", keyword=keyword, poems=poems)

@app.route('/result/content=<content>/page=<page>', methods=['GET'])
def result_content(page,content):
    if content == 'content':
        direction = 5
    elif content == 'name':
        direction = 1
    elif content == 'poet':
        direction = 2
    else:
        direction = 4
    keyword = request.args.get('keyword')
    if direction != 2:
        poems = es_search(keyword,int(page),direction)
        return render_template("result_poetry.html", keyword=keyword, poems=poems,page = int(page))
    else:
        poets = search_poet(keyword,int(page))
        return render_template("result_poet.html", keyword=keyword, poets=poets,page = int(page))

@app.route('/author/',methods = ['GET'])
def poet_all():
    return redirect("/author/dynasty=不限/page=1")

@app.route('/author/dynasty=<dyn>/page=<page>',methods = ['GET'])
def poet_all_dynasty(dyn,page):
    poet_tuple = select_author(dyn,page)
    return render_template('poet_all_new.html',dynasty = dyn,data = poet_tuple,page = int(page))


@app.route('/poetry/',methods = ['GET'])
def poetry_all():
    return redirect("/poetry/dynasty=不限/page=1")

@app.route('/poetry/dynasty=<dyn>/page=<page>',methods = ['GET'])
def poetry_all_dynasty(dyn,page):
    data_list = select_poetry(dyn,page)
    
    
    return render_template('poetry_all.html',dynasty = dyn,page = int(page),data = data_list[0],\
                                            tag_list = data_list[1],length = data_list[2],type_list = data_list[3])


@app.route('/poetry/poetryId=<poetryId>',methods = ['GET'])
def poetry_detail(poetryId):
    data_list = select_poetryId(poetryId)
    poetry = data_list[0]
    intro_poet = data_list[1]
    return render_template('poetry_detail.html',title = poetry[7],tags = json.loads(poetry[3]),intro_poet = intro_poet,\
                                                fanyi = json.loads(poetry[5]),content = json.loads(poetry[4]),\
                                                shangxi = json.loads(poetry[6]),author = poetry[1])

@app.route('/author/poetid=<poetid>')
def poet(poetid):
    data_list = select_poetid(poetid)
    
    

    return render_template('poet_detail.html',name = data_list[0],intro = data_list[1],sum = data_list[2],\
        detail_info = data_list[3],poetid = poetid,img = data_list[4])

@app.route("/data/<name>",methods = ['GET'])
def get_data1(name):
    
    return json.dumps(get_graph_data1(name))

@app.route("/data2/<name>",methods = ['GET'])
def get_data2(name):
    
    return json.dumps(get_graph_data(name))


@app.route('/poetry/poetid=<poetid>/page=<page>',methods = ['GET'])
def poetry_of_poet(poetid,page):
    data_list = select_poemofPoet(poetid,page)
    return render_template('poetry_of_poet.html',dynasty = data_list[0],page = int(page),poetid = poetid,type_list = data_list[1],\
                            poet = data_list[2],data = data_list[3],tag_list = data_list[4],length = data_list[5])


@app.route('/poetry/type=<typ>/page=<page>',methods = ['GET'])
def poetry_all_type(typ,page):
    
    data_list = select_type(typ,page)

    
    return render_template('poetry_all_type.html',type = typ,type_list = data_list[0],page = int(page),data = data_list[1],\
                            tag_list = data_list[2],length = data_list[3],dynasty_list = data_list[4]    )
                              
@app.route('/varses/page=<page>',methods = ['GET'])
def varses(page):
    varses_list = select_varses(page)

    return render_template('varses.html',varses_list = varses_list,page = int(page))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5000,debug = True)