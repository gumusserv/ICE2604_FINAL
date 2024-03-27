import asyncio
import aiohttp
import json
import time
import requests
from lxml import etree 

CONCURRENCY = 200
semaphore = asyncio.Semaphore(CONCURRENCY)
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47'}

mingju_dic = {}
session=None
id=1
origin_link = "https://so.gushiwen.cn/mingjus/default.aspx?page="

def get_all_aouthors_and_tags():
    response = requests.get("https://so.gushiwen.cn/mingjus/", headers = headers)
    response.encoding = 'utf-8'
    tree_info = etree.HTML(response.text)
    tags_list = tree_info.xpath('//div[@class="main3"]/div[@class="right"]/div[@class="sons"][1]/div[@class="cont"]/a/text()')
    authors_list= tree_info.xpath('//div[@class="main3"]/div[@class="right"]/div[@class="sons"][2]/div[@class="cont"]/a/text()')
    print(authors_list, tags_list)
    return authors_list, tags_list





def get_all_mingju(url,headers):
    global id,page
    global mingju_dic
    page=1
    while True:
        new_response=requests.get(url=origin_link+str(page)+url, headers=headers)
        new_response.encoding = 'utf-8'
        new_tree = etree.HTML(new_response.text)
        num = len(new_tree.xpath('//div[contains(@style,"margin-top:12px;")]'))
        if num == 0:
            break
        for i in range(num):
            i+=1
            mingju_list = new_tree.xpath('//div[contains(@style,"margin-top:12px;")][{}]/a/text()'.format(str(i)))
            varse=mingju_list[0]
            if len(mingju_list) == 2:
                source=mingju_list[1]
            else:
                source="None"
        
            mingju_dic[id]={}
            mingju_dic[id]["varse"]=varse
            mingju_dic[id]["source"]=source
            print(mingju_dic[id])
            id+=1
            
        if page == 10:
            break
        page+=1


def main():


    authors_list, tags_list = get_all_aouthors_and_tags()
    for _ in authors_list:
        get_all_mingju("&tstr=&astr={}&cstr=&xstr=".format(_),headers)
        print("爬取{}的名句成功".format(_))
    for _ in tags_list:
        get_all_mingju("&tstr={}&astr=&cstr=&xstr=".format(_),headers)
        print("爬取{}的名句成功".format(_))

    with open('./famous_verses/famous_verses.json',"w",encoding = "utf-8") as fp:
       json.dump(mingju_dic,fp = fp,indent = 2,sort_keys= True,ensure_ascii = False)
    print("complete")


if __name__ == "__main__":
    main()