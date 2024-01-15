import asyncio
import aiohttp
import json
import time
from lxml import etree 

CONCURRENCY = 200
semaphore = asyncio.Semaphore(CONCURRENCY)
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47'}

mingju_dic = {}
session=None
id=1
page=1

async def get_all_mingju(url,headers):
    global id,page
    global mingju_dic
    async with semaphore:
        try:
            async with session.get(url, headers=headers) as new_response:
                new_response.encoding = 'utf-8'
                text = await new_response.text()
                new_tree = etree.HTML(text)
                for i in range(50):
                    i+=1

                    mingju_list = new_tree.xpath('//div[@class="cont mj_wrap"][{}]/a/text()'.format(str(i)))
                    varse=mingju_list[0]
                    if len(mingju_list) == 2:
                        source=mingju_list[1]
                    else:
                        source="None"
                
                    mingju_dic[id]={}
                    mingju_dic[id]["varse"]=varse
                    mingju_dic[id]["source"]=source
                    id+=1

                print("爬取{}页成功".format(page))
                page+=1
        except:
            print("一共有{}页".format(page))

async def main():
    global session
    session = aiohttp.ClientSession()

    scrape_index_tasks = [asyncio.ensure_future(get_all_mingju("https://shiwens.com/mingju_{}.html".format(_),headers)) for _ in range(1, 1001)]
    await asyncio.gather(*scrape_index_tasks)

    with open('./verses/verses.json',"w",encoding = "utf-8") as fp:
       json.dump(mingju_dic,fp = fp,indent = 2,sort_keys= True,ensure_ascii = False)
    await session.close()

if __name__ == "__main__":
    t1 = time.time()
    asyncio.get_event_loop().run_until_complete(main())
    t2 = time.time()
    print("一共花费{}秒".format(t2-t1))