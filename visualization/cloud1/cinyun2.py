from stylecloud import gen_stylecloud
import random
import re

# 读取数据
with open('yixiang.txt', encoding='utf-8') as f:
    data = f.read()
new_data = re.findall('[\u4e00-\u9fa5]+', data, re.S)
new_data = " ".join(new_data)
#print(new_data)

# 文本预处理  去除一些无用的字符   只提取出中文出来

#print(result_list)

# 将palettable配色方案 1587类弄到了本地txt里  读取配色方案
with open('palettable配色方案.txt') as f:
    choices = f.read().split('\n')[:-1]
#print(choices)

# 个人推荐使用的palette配色方案
# colorbrewer.qualitative.Dark2_7
# cartocolors.qualitative.Bold_5
# colorbrewer.qualitative.Set1_8

gen_stylecloud(
    text=data,               # 文本数据
    
    size=800,                                 # 词云图大小
    font_path='simhei.ttf',   # 中文词云  显示需要设置字体
    output_name='cloud2.png',                   # 输出词云图名称
    # icon_name='fas fa-map',             # 图标
    icon_name='fas fa-rocket',
    gradient='horizontal',
    palette=random.choice(choices)            # 随机选取配色方案

)