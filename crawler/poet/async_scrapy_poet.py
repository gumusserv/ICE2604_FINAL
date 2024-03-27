import asyncio
import aiohttp
import json
import time
import requests
from lxml import etree 

CONCURRENCY = 200
semaphore = asyncio.Semaphore(CONCURRENCY)
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47'}

session=None

poet_dic = {}
id = 1
origin_link="https://shiwens.com"


# scrapy the link of detail information link of all poet
async def get_poet_link(dynasty, page):
    global poet_dic, id, headers
    async with semaphore:
        for i in range(1,page+1):
            async with session.get("https://shiwens.com/authors_{}.html?cd={}".format(str(i),dynasty),headers=headers) as response:
                response.encoding = 'utf-8'
                text = await response.text()
                tree = etree.HTML(text)
                poet_link_list = tree.xpath('//div[@class="sonspic"]/div[1]/p[1]/a[1]/@href')
                poet_list = tree.xpath('//div[@class="sonspic"]/div[1]/p[1]/a[1]/b/text()')
                for i in range(len(poet_list)):
                    poet_dic[id] = {"name":poet_list[i], "poetlink":origin_link+poet_link_list[i], "dynasty":dynasty}
                    id+=1


# get ajax information
def get_per_info(info_link):
    response_info = requests.get("https://shiwens.com/ziliao/ajax_content.html?id={}".format(info_link[5:]), headers = headers)
    response_info.encoding = 'utf-8'
    tree_info = etree.HTML(response_info.text)
    info_title_list = tree_info.xpath('//h2/span/text()')
    info_content = tree_info.xpath('//div[@class="contyishang"]/p//text() | //div[@class="contyishang"]/text()')
    info_content = [info  for info in info_content if info!=[]]
    return info_title_list[0], info_content


# scrapy the detail information of per poet
async def get_info(poetid):
    global poet_dic, id, headers
    print("开始爬取{}！".format(poet_dic[poetid]["name"]))
    async with semaphore:
        async with session.get(poet_dic[poetid]["poetlink"],headers=headers) as response:
            response.encoding = 'utf-8'
            text = await response.text()
            tree = etree.HTML(text)

            # scrapy the avatar of poet
            try:
                poet_avatar_link = tree.xpath('//div[@class="sonspic"]/div[1]/div[1]/img/@src')
                poet_dic[poetid]["avatar_link"] = origin_link+poet_avatar_link[0]
            except:
                poet_dic[poetid]["avatar_link"] = "None"

            # scrapy the brief introduction of poet
            try:
                poet_brief_intro = tree.xpath('//div[@class="sonspic"]/div[1]/p/text()')
                poet_dic[poetid]["brief_intro"] = poet_brief_intro[0]
            except:
                poet_dic[poetid]["brief_intro"] = "None"

            # scrapy the poetry link of poet
            try:
                poetry_link = tree.xpath('//div[@class="sonspic"]/div[1]/a/@href | //div[@class="sonspic"]/div[1]/p//@href')
                poet_dic[poetid]["poetry_link"] = origin_link+poetry_link[0]
            except:
                poet_dic[poetid]["poetry_link"] = "None"

            # scrapy the detail infomation of poet
            try:
                detail_info = {}
                info_list = tree.xpath('//div[@style="position:relative; z-index:0px;"]/@id')
                for info_link in info_list:
                    info_title, info_content=get_per_info(info_link)
                    detail_info[info_title]=info_content
                poet_dic[poetid]["detail_info"] = detail_info
                if poet_dic[poetid]["detail_info"] == {}:
                    poet_dic[poetid]["detail_info"] = "None"
            except:
                poet_dic[poetid]["detail_info"] = "None"

            print("爬取{}成功！！".format(poet_dic[poetid]["name"]))
  

async def main():
    global session
    session = aiohttp.ClientSession()

    # init data
    # dynasty_list = ['唐代','宋代','魏晋','近现代','南北朝','清代','明代','元代','两汉','五代','先秦','金朝','隋代']
    dynasty_list = ['先秦']
    # page_num_dynasty = [206,246,19,2,27,353,240,58,11,7,2,16,5]
    page_num_dynasty = [2]

    scrape_index_task1 = [asyncio.ensure_future(get_poet_link(dynasty_list[i],page_num_dynasty[i])) for i in range(len(dynasty_list))]
    await asyncio.gather(*scrape_index_task1)
    print("complete task1!")

    scrape_index_task2 = [asyncio.ensure_future(get_info(poetid)) for poetid in range(1,id)]
    await asyncio.gather(*scrape_index_task2)
    with open('./poet/poet3.json',"w",encoding = "utf-8") as fp:
       json.dump(poet_dic,fp = fp,indent = 2,sort_keys= True,ensure_ascii = False)
    print("complete task2!")

    await session.close()

if __name__ == "__main__":
    t1 = time.time()
    asyncio.get_event_loop().run_until_complete(main())
    total = len(poet_dic)
    t2 = time.time()
    print("爬取{}个诗人用时: {}s".format(str(total),str(t2 - t1)))