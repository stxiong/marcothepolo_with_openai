import datetime
import json
import openai
import os
import time
import pymongo

openai.api_key = "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"
mongo_cli = pymongo.MongoClient("localhost", 27017)
product_db = mongo_cli['1688_product_test']
product_db.product_info.create_index([('item_id', pymongo.ASCENDING)], unique=True)



    
prompt_generate_keywords_of_selling_points = "here are a list of products of a clothing supplier, \
    please extract out 10 keywords as the best selling points for this supplier, \
    and generate a short recommend text in english for this clothing supplier, \
    and please notice that don't include any information about 'cross-border': %s"

def parse_product(item_id, category, title, item_specifies):
    
    gpt_content_dict = {}
    
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_generate_product_title%(category, title, json.dumps(item_specifies)),
      max_tokens=128,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    gpt_title = response.choices[0]['text']
    print ("the original title : %s"%title)
    print ("the title generate by GPT-3 is: %s"%gpt_title.strip())

    gpt_content_dict['title'] = gpt_title.strip()

    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_generate_style%(title, json.dumps(item_specifies)),
      max_tokens=128,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    style_ret = response.choices[0]['text']
    print(style_ret)
    
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_extract_item_specifies%(title, json.dumps(item_specifies)),
      max_tokens=1024,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    print(response.choices[0]['text'])
    
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_expand_tags%(title, json.dumps(item_specifies), style_ret),
      max_tokens=1024,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    print(response.choices[0]['text'])


    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_generate_recommend_essay%(title, json.dumps(item_specifies)),
      max_tokens=256,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    print(response.choices[0]['text'])

    return gpt_content_dict



def store_data_in_mongodb(product_json, gpt_content_dict):
    timestamp_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')


with open("1688_product_test.json", "r") as file_in:
    gpt_title_list = []
    cc = 0
    for line in file_in.readlines():
        try:
            product_json = json.loads(line)
            product_json = dict(product_json)
            cc += 1
            print("%d.....%s"%(cc, product_json['itemId']))
            gpt_content_dict = parse_product(
                "clothes", 
                product_json['itemId'], 
                product_json['itemName'], 
                product_json['itemSpecifics']
            )
            store_data_in_mongodb(product_json, gpt_content_dict)

            gpt_title_list.append(gpt_title)
            product_db.product_info.insert_one({
                "item_id": product_json['itemId'],
                "title": product_json['itemName'],
                "gpt_title": gpt_title,
                "timestamp": timestamp_str
            })
            print("success!!!!!!.........")
        except Exception as e:
            print("error!!!!!!.........")
            print(e)
    
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_generate_keywords_of_selling_points%','.join(gpt_title_list),
      max_tokens=512,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    print(response.choices[0]['text'])



file_in.close()
