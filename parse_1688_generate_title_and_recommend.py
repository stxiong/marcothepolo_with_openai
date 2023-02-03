import os
import openai
import time
import datetime
import json

openai.api_key = "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"

prompt_generate_product_title = "this is some information of a clothes product in json format, \
    please help to genenrate a product title in english, \
    and please notice that don't include any information about 'cross-border': %s %s"

prompt_extract_item_specifies = "this is some information of a clothes product in json format, \
    please list out all the specifies in english: %s %s"

prompt_generate_style = "this is some information of a clothes product in json format, \
    please tell me what's the style of this product in English, \
    and please notice that don't include any information about 'cross-border': %s %s"


prompt_expand_tags = "this is some information of a clothes product in json format\
    , please extract the tags for describing its style in English \
    , and for every tag please help me to list out most usual synonyms \
    : %s %s %s"
    
prompt_generate_recommend_essay = "this is some information of a clothes  product in json format, \
    please help to generate a short recomend text in english, for online selling: %s %s"
    
prompt_generate_keywords_of_selling_points = "here are a list of products of a clothing supplier, \
    please extract out 10 keywords as the best selling points for this supplier, \
    and generate a short recommend text in english for this clothing supplier, \
    and please notice that don't include any information about 'cross-border': %s"

def parse_product(item_id, title, item_specifies):
    
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

    return gpt_title

with open("1688_product_test.json", "r") as file_in:
    gpt_title_list = []
    cc = 0
    for line in file_in.readlines():
        try:
            product_json = json.loads(line)
            product_json = dict(product_json)
            cc += 1
            print("%d.....%s"%(cc, product_json['itemId']))
            gpt_title = parse_product(product_json['itemId'], product_json['itemName'], product_json['itemSpecifics'])
            gpt_title_list.append(gpt_title)
        except Exception as e:
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
