import asyncio
import aiohttp
import json
import time
import requests
import psutil
import os
import copy
from lxml import etree 

CONCURRENCY = 100
semaphore = asyncio.Semaphore(CONCURRENCY)
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47'}

timeout = aiohttp.ClientTimeout(total=20)
# connector = aiohttp.TCPConnector(limit=50,force_close=True) 

session=None


# get ajax information
def get_per_info(info_link):
    response_info=requests.get(info_link, headers = headers)
    response_info.encoding = 'utf-8'
    tree_info = etree.HTML(response_info.text)
    info_title_list = tree_info.xpath('//h2/span/text()')
    info_content = tree_info.xpath('//div[@class="contyishang"]/p//text() | //div[@class="contyishang"]/text()')
    info_content = [info  for info in info_content if info!=[]]
    return info_title_list[0], info_content


# scrapy the detail information of per poet
async def get_info(poetryid):
    global poetry_dic,  headers, dic_poetrys_link
    print("开始爬取{}！".format(dic_poetrys_link[str(poetryid)]["name"]))
    async with semaphore:
        try:
            async with session.get(dic_poetrys_link[str(poetryid)]["poetrylink"],headers=headers) as response:
                response.encoding = 'utf-8'
                text = await response.text()
                tree = etree.HTML(text)
                poetry_dic[poetryid] = copy.deepcopy(dic_poetrys_link[str(poetryid)])
                # scrapy the content of the poetry
                try:
                    poetry_content = tree.xpath('//div[@class="main3"]/div[1]/div[1]/div[1]/div[@class="contson"]//text()')
                    poetry_dic[poetryid]["content"] = poetry_content
                except:
                    poetry_dic[poetryid]["content"] = "None"

                # scrapy the dynasty of the poetry
                try:
                    poetry_dynasty = tree.xpath('//div[@class="main3"]/div[1]/div[1]/div[1]/p//text()')[0]
                    poetry_dic[poetryid]["dynasty"] = poetry_dynasty
                except:
                    poetry_dic[poetryid]["dynasty"] = "None"

                # scrapy the author of the poetry
                try:
                    poetry_author = tree.xpath('//div[@class="main3"]/div[1]/div[1]/div[1]/p//text()')[2]
                    poetry_dic[poetryid]["author"] = poetry_author
                except:
                    poetry_dic[poetryid]["author"] = "None"

                # scrapy the tags of the poetry
                try:
                    poetry_tags = tree.xpath('//div[@class="tag"]/a//text()')
                    if poetry_tags == []:
                        poetry_dic[poetryid]["tags"] = "None"
                    else:
                        poetry_dic[poetryid]["tags"] = poetry_tags
                except:
                    poetry_dic[poetryid]["tags"] = "None"

                # scrapy the fanyi of the poet
                try:
                    info_link = tree.xpath('//div[contains(@id, "fanyi")]/@id')[0]
                    info_link = "https://shiwens.com/fanyi/ajax_content.html?id={}".format(info_link[5:])
                    info_title, info_content=get_per_info(info_link)    
                    poetry_dic[poetryid]["fanyi"] = {info_title:info_content}
                except:
                    poetry_dic[poetryid]["fanyi"] = "None"

                # scrapy the shangxi of the poet
                try:
                    detail_info = {}
                    info_list = tree.xpath('//div[contains(@id, "shangxi")]/@id')
                    info_list = [info for info in info_list if info[0:8] != "shangxiq"]
                    for info_link in info_list:
                        info_link = "https://shiwens.com/shangxi/ajax_content.html?id={}".format(info_link[7:])
                        info_title, info_content=get_per_info(info_link)    
                        detail_info[info_title]=info_content
                    poetry_dic[poetryid]["shangxi"] = detail_info
                    if detail_info == {}:
                        poetry_dic[poetryid]["shangxi"] = "None"
                except:
                    poetry_dic[poetryid]["shangxi"] = "None"
                print("爬取{}成功！！".format(dic_poetrys_link[str(poetryid)]["name"]))
        except:
            with open('./poem/error_id.txt','a',encoding='utf-8') as f:
                f.write("爬取第{}首诗歌失败!!!".format(str(poetryid)) + '\n')
            print("连接{}失败！！".format(dic_poetrys_link[str(poetryid)]["poetrylink"]))

  

async def main():
    global session, poetry_dic, dic_poetrys_link
    session = aiohttp.ClientSession(timeout=timeout)
    poetry_dic ={}

    with open("./poem/poetry_todo1.json",encoding = "utf-8") as fp:
        dic_poetrys_link = json.load(fp)
    length = len(dic_poetrys_link)

    # scrapy 10000 poetries once a time 
    for i in range(30001, length, 10000):
        beginnum = i
        endnum = i+10000-1
        if endnum > length:
            endnum = length

        # task1
        scrape_index_task2 = [asyncio.ensure_future(get_info(poetryid)) for poetryid in range(beginnum,endnum+1)]
        await asyncio.gather(*scrape_index_task2)
        print("complete {}-{} task1!".format(str(beginnum),str(endnum)))

        #task2
        with open('./poem/poetry/poetry_{}-{}.json'.format(str(beginnum),str(endnum)),"w",encoding = "utf-8") as fp:
            json.dump(poetry_dic,fp = fp,indent = 2,sort_keys= True,ensure_ascii = False)
        print("complete {}-{} task2!".format(str(beginnum),str(endnum)))
        
        # print(u'当前进程的内存使用：%.4f GB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) )
        poetry_dic.clear()
        # print(u'当前进程的内存使用：%.4f GB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) )

    await session.close()


if __name__ == "__main__":
    t1 = time.time()
    asyncio.get_event_loop().run_until_complete(main())
    t2 = time.time()
    print("爬取用时: {}s".format(str(t2 - t1)))