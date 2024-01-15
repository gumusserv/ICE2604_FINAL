import asyncio
import aiohttp
import json
import time
import requests
from lxml import etree 

CONCURRENCY = 200
semaphore = asyncio.Semaphore(CONCURRENCY)
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47'}

# timeout = aiohttp.ClientTimeout(total=1200)
# connector = aiohttp.TCPConnector(limit=50,force_close=True) 

session=None

poetry_dic = {}
poetry_id = 1
origin_link="https://shiwens.com"


# scrapy the link of each poetry
async def get_each_poetry_link(poetry_link_of_poet, poetid):
    global poetry_dic, poetry_id, headers
    async with semaphore:
        async with session.get(poetry_link_of_poet,headers=headers) as page_response:
            page_response.encoding = 'utf-8'
            page_text = await page_response.text()
            page_tree = etree.HTML(page_text)
            try:
                page = int(page_tree.xpath('//label[@id="sumPage"]/text()')[0])
            except:
                print(poetid)
                page=0
        for i in range(1,page+1):
            async with session.get(poetry_link_of_poet[:-5]+"_"+str(i)+".html",headers=headers) as response:
                response.encoding = 'utf-8'
                text = await response.text()
                tree = etree.HTML(text)
                poetry_link_list = tree.xpath('//a[@class="shi_title"]/@href')
                poetry_list = tree.xpath('//a[@class="shi_title"]//text()')
                for i in range(len(poetry_list)):
                    poetry_dic[poetry_id] = {"name":poetry_list[i], "poetrylink":origin_link+poetry_link_list[i], "authorid":poetid}
                    poetry_id+=1
        print("爬取第{}位诗人的诗歌链接成功！！".format(poetid))
        
  

async def main():
    global session
    session = aiohttp.ClientSession()

    # data init
    with open("./poet/poet.json",encoding = "utf-8") as fp:
        dic_poets = json.load(fp)
    num_poet = len(dic_poets)   
    # num_poet = 1000

    # task1
    scrape_index_task1 = [asyncio.ensure_future(get_each_poetry_link(dic_poets[str(poetid)]["poetry_link"],poetid)) for poetid in range(1,num_poet+1)]
    await asyncio.gather(*scrape_index_task1)
    print("complete task1!")
    with open('./poem/poetry_todo1.json',"w",encoding = "utf-8") as fp:
       json.dump(poetry_dic,fp = fp,indent = 2,sort_keys= True,ensure_ascii = False)

    #task3
    with open('./poem/poetry_link_to_scrapy.json',"w",encoding = "utf-8") as fp:
       json.dump(poetry_dic,fp = fp,indent = 2,sort_keys= True,ensure_ascii = False)
    print("complete task3!")

    await session.close()

if __name__ == "__main__":
    t1 = time.time()
    asyncio.get_event_loop().run_until_complete(main())
    total = len(poetry_dic)
    t2 = time.time()
    print("爬取{}首诗的链接用时: {}s".format(str(total),str(t2 - t1)))