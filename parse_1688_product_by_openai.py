import os
import openai
import time
import datetime
import json

openai.api_key = "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"

def parse_product(item_id, title, item_specifies):
    print(item_id)
    
    prompt = "this is some information of a product in json format, please help to genenrate a product title in english: %s %s"%(title, json.dumps(item_specifies))
    print ("...%s..."%prompt)
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

    print("-----------------------------------------------------------")
    prompt = "this is some information of a product in json format, please list out all the specifies in english: %s %s"%(title, json.dumps(item_specifies))
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      max_tokens=1000,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    print(response.choices[0]['text'])

    print("-----------------------------------------------------------")
    prompt = "this is some information of a product in json format, please help to generate three paragraphs of recomend text in english, for online selling: %s %s"%(title, json.dumps(item_specifies))
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      max_tokens=1000,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    print(response.choices[0]['text'])

with open("1688.json", "r") as file_in:
    content = file_in.read()
#    content = '{"platform":"abc"}'
    product_json = json.loads(content)
    product_json = dict(product_json)
    print(product_json['itemName'])
    print(product_json['itemSpecifics'])
    parse_product(product_json['itemId'], product_json['itemName'], product_json['itemSpecifics'])

file_in.close()
