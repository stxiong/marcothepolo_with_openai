import datetime
import json
import openai
import os
import time
import pymongo

openai.api_key = "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"
OPENAI_GPT_MODEL = "text-davinci-003" 

mongo_cli = pymongo.MongoClient("localhost", 27017)
product_db = mongo_cli['1688_product_test']
product_table = product_db['gpt_product_info_beam']
product_table.create_index([('item_id', pymongo.ASCENDING)], unique=True)


def parse_specific_dict(item_specifies):
    result = {}
    for kv in item_specifies:
        result[kv['name']] = kv['value']
    print(result)
    return result
        
     

def parse_product(category, item_id, item_title, item_specifies):
    
    gpt_content_dict = {}
   
    # 1.generate short product title in English
    print("...#1.generate short product title in English")
    response = openai.Completion.create(
      model=OPENAI_GPT_MODEL,
      prompt="this is some information of a %s product in json format, \
        please help to genenrate a product title in english, \
        and please notice that don't include any information \
        about 'cross-border': %s %s"%(category, item_title, json.dumps(item_specifies)),
      max_tokens=16,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    gpt_title = response.choices[0]['text']
    gpt_content_dict['short_title'] = gpt_title.strip()
    print(response.choices)
    print(response.usage)
    
    # 2.generate long product title in English
    print("...#2.generate long product title in English")
    response = openai.Completion.create(
      model=OPENAI_GPT_MODEL,
      prompt="this is some information of a %s product in json format, \
        please help to genenrate a product title in english, \
        and please notice that don't include any information \
        about 'cross-border': %s %s"%(category, item_title, json.dumps(item_specifies)),
      max_tokens=64,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    gpt_title = response.choices[0]['text']
    gpt_content_dict['long_title'] = gpt_title.strip()
    print(response.choices)
    print(response.usage)

    
    print ("the original title : %s"%item_title)
    print ("the short title generate by GPT-3 is: %s"%gpt_content_dict['short_title'].strip())
    print ("the long title generate by GPT-3 is: %s"%gpt_content_dict['long_title'].strip())
    
    # 3.extract item specifies in English
    print("...#3.extract item specifies in English")
    prompt = "this is some information of a %s product in json format, \
        please list out all the specifies in english: %s %s"%(category, item_title, json.dumps(item_specifies))
    print(prompt)
    response = openai.Completion.create(
      model=OPENAI_GPT_MODEL,
      prompt=prompt,
      max_tokens=1024,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0)
    gpt_content_dict['item_specifies'] = response.choices[0]['text']
    print(response.choices)
    print(response.usage)
    
    
    # 4. select import tags 
    print("...#4.select import tags")
    prompt = "this is some information of a %s product in json format \
        , please extract no more than 10 most important tags for describing this online product in English \
        : %s %s"%(category, item_title, json.dumps(item_specifies))
    print(prompt)
    response = openai.Completion.create(
      model=OPENAI_GPT_MODEL,
      prompt=prompt,
      max_tokens=1024,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    gpt_content_dict['selected_tags'] = response.choices[0]['text']
    print(response.choices)
    print(response.usage)


    # 5. generate recommend essay
    print("...#5.generate recommend essay")
    prompt="this is some information of a %s product in json format, \
        please help to generate a short recomend text in english, \
        for online selling: %s %s"%(category, item_title, json.dumps(item_specifies))
    print(prompt)
    response = openai.Completion.create(
      model=OPENAI_GPT_MODEL,
      prompt=prompt,
      max_tokens=256,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    gpt_content_dict['recommend_essay'] = response.choices[0]['text']
    print(response.choices)
    print(response.usage)

    return gpt_content_dict



def store_data_in_mongodb(product_json, gpt_content_dict):
    timestamp_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            
    product_table.insert_one({
        "item_id": product_json['itemId'],
        "item_name": product_json['itemName'],
        "item_view_url": product_json['itemViewUrl'],
        "priority": product_json['priority'],
        "seller_id": product_json['sellerId'],
        "seller_name": product_json['sellerName'],
        "seller_link": product_json['sellerLink'],
        "gpt_content": gpt_content_dict,
        "timestamp": timestamp_str
    })


c_all = 0
c_exit = 0
c_success = 0
c_error = 0
with open("1688_product_beam.json", "r") as file_in:
#with open("1688_product_test.json", "r") as file_in:
    for line in file_in.readlines():
#        c_all += 1
#        try:
            product_json = json.loads(line)
            product_json = dict(product_json)
            if product_table.find_one({'item_id': product_json['itemId']}) == None: 
                print("%d.....%s"%(c_all, product_json['itemId']))
                item_specific_dict = parse_specific_dict(product_json['itemSpecifics'])
                gpt_content_dict = parse_product(
                    "clothes", 
                    product_json['itemId'], 
                    product_json['itemName'],
#                    product_json['itemSpecifics'],
                    item_specific_dict
                )
                store_data_in_mongodb(product_json, gpt_content_dict)
                c_success += 1
#            else:
#                c_exit += 1
#        except Exception as e:
#            c_error += 1
#            print("error....%s"%e)
#        print("%d items processed: %d exist, %d success, %d error."%(c_all, c_exit, c_success, c_error))
file_in.close()

print("%d items process: %d exist, %d success, %d error."%(c_all, c_exit, c_success, c_error))
