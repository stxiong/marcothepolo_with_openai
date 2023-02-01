import os
import openai
import time
import datetime
import json

openai.api_key = "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"

def parse_product(item_id, title, item_specifies):
    print(item_id)
    
    prompt = "this is some information of a product in json format, please help to genenrate a product title in english: %s %s"%(title, json.dumps(item_specifies))
    #print ("...%s..."%prompt)
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      max_tokens=300,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    gpt_title = response.choices[0]['text']
    print ("the original title : %s"%title)
    print ("the title generate by GPT-3 is: %s"%gpt_title.strip())

#    print("-----------------------------------------------------------")
#    prompt = "this is some information of a product in json format, please list out all the specifies in english: %s %s"%(title, json.dumps(item_specifies))
#    response = openai.Completion.create(
#      model="text-davinci-003",
#      prompt=prompt,
#      max_tokens=1000,
#      top_p=1.0,
#      frequency_penalty=0.0,
#      presence_penalty=0.0
#    )
#    print(response.choices[0]['text'])
#
#    prompt = "this is some information of a product in json format, please help to generate a short recomend text in english, for online selling: %s %s"%(title, json.dumps(item_specifies))
#    response = openai.Completion.create(
#      model="text-davinci-003",
#      prompt=prompt,
#      max_tokens=300,
#      top_p=1.0,
#      frequency_penalty=0.0,
#      presence_penalty=0.0
#    )
#    print(response.choices[0]['text'])
#
#    print("-----------------------------------------------------------")
#    prompt = "this is some information of a product in json format, please help to generate three paragraphs of recomend text in english, for online selling: %s %s"%(title, json.dumps(item_specifies))
#    response = openai.Completion.create(
#      model="text-davinci-003",
#      prompt=prompt,
#      max_tokens=300,
#      top_p=1.0,
#      frequency_penalty=0.0,
#      presence_penalty=0.0
#    )
#    print(response.choices[0]['text'])

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
    
    title_string = ','.join(gpt_title_list)
    prompt = "here are a list of products from a online store, please extract out 10 keywords as the best selling points for this store: %s"%title_string
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      max_tokens=300,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    print(response.choices[0]['text'])



file_in.close()
