from elasticsearch import Elasticsearch
import json
import pandas as pd
import os

# Preparation

es = Elasticsearch('http://localhost:9200', basic_auth=('defalt', '123456'))
print(es.ping())

file_famous = "crawler/famous_verses/famous_verses.json"
file_poetry_list = []
file_poet = "crawler/poet/poet.json"
file_verses = "crawler/verses/verses.json"

file_example = "crawler/poem/poetry/poetry_1-10000.json"

class FilefailError():{}



# Delete former
es.indices.delete(index="poetry")







# Reading files
df = pd.read_json(file_example)

if (not df.empty):
    print("Opened successfully.")
else:
    raise FilefailError()

count = 0

for item in df.items():
    count+=1
    local_dict = item[1].to_dict()
    another_dict = dict()
    for (key, value) in local_dict.items():
        if (type(value)==dict):
            for (k,v) in value.items():
                another_dict[key] = v
                break
        else:
            another_dict[key] = value
    es.index(index="poetry", document=another_dict, id=count)

print(count)