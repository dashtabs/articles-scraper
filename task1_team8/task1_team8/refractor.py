import os
import json
import codecs

json_path = os.path.dirname(os.path.realpath(__file__))+"\\"
json_file = "result.json"
json_data=[]
os.mkdir(json_path+"final_txt")
with open(json_path+json_file, encoding='utf-8') as json_fileopen:
    json_data = json.load(json_fileopen)
for article in json_data:
    if isinstance(article['article_text'], list):
        article['article_title'] = " ".join(article["article_title"])
        article['article_text'] = " ".join(article["article_text"])
    article_text = article["article_title"] + "\n\n" + article['article_text'].replace("\xa0"," ")
    article_uuid = article['article_uuid']
    with codecs.open(json_path+"final_txt/"+article_uuid+".txt", "w", "utf-8-sig") as temp:
        temp.write(article_text)
