import os
import openai
import time
import datetime
import json

openai.api_key = "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"

prompt_generate_product_title = "this is some information of a product in json format, \
    please help to genenrate a product title in english: %s %s"

prompt_extract_item_specifies = "this is some information of a product in json format, \
    please list out all the specifies in english: %s %s"

prompt_expand_tags = "this is some information of a product in json format\
    , please extract no more than 20 most important tags for online selling in English\
    , and for every tag please help me to list out most usual synonyms \
    : %s %s"
    
prompt_generate_recommend_essay = "this is some information of a product in json format, \
    please help to generate a short recomend text in english, for online selling: %s %s"
    
prompt_generate_keywords_of_selling_points = "here are a list of products from a online store, \
    please extract out 10 keywords as the best selling points for this store: %s"

def parse_product(item_id, title, item_specifies):
    print(item_id)
    
    #print ("...%s..."%prompt)
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_generate_product_title%(title, json.dumps(item_specifies)),
      max_tokens=128,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    gpt_title = response.choices[0]['text']
    print ("the original title : %s"%title)
    print ("the title generate by GPT-3 is: %s"%gpt_title.strip())

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
      prompt=prompt_expand_tags%(title, json.dumps(item_specifies)),
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

    return gpt_title

with open("1688_product_test.json", "r") as file_in:
    gpt_title_list = []
    for line in file_in.readlines():
        product_json = json.loads(line)
        product_json = dict(product_json)
#        print(product_json['itemName'])
#        print(product_json['itemSpecifics'])
        gpt_title = parse_product(product_json['itemId'], product_json['itemName'], product_json['itemSpecifics'])
        gpt_title_list.append(gpt_title)
    
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
