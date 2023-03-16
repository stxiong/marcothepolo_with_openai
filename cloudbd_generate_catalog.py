import csv
import os
import openai
import time
import datetime

openai.api_key = "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"

prompt_generate_product_recommend = "I am an offline shop named '%s' from %s,\
    the main category I sell is %s and I want to sell something new to improve my business, \
    what top 10 keywords of products do you recommend? and what is the best price range? \
    and please tell me why should i sell this in my city."

prompt_generate_product_recommend_by_full_info = "here is the information of my shop, \
    please tell me what top 10 keywords of products do you recommend? \
    and please tell me why should i sell this in my city: %s"

prompt_extract_keyword_from_comment = "here is a comment from yelp for my shop, \
    please extract out the key information for this comment: %s"

def generate_recommend_for_shop(name, category, city):
    
    #print ("...%s..."%prompt)
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_generate_product_recommend%(name, city, category),
      max_tokens=300,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    recommend_text = response.choices[0]['text']
    print ("the recommend generate for [%s][%s] from [%s] by GPT-3 is: %s"%(name, category, city, recommend_text.strip()))


def generate_recommend_for_shop_by_full_info(shop_info):
    
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_generate_product_recommend_by_full_info%(shop_info),
      max_tokens=300,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    recommend_text = response.choices[0]['text']
    print ("the recommend generate for by GPT-3 is: %s"%(recommend_text.strip()))

def extract_keyword_from_comment(comment):
    
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_extract_keyword_from_comment%(comment),
      max_tokens=300,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    recommend_text = response.choices[0]['text']
    print ("the keywords generate for by GPT-3 is: %s"%(recommend_text.strip()))

with open('cloudbd_shops_test.csv', newline='') as csv_reader:
    gpt_title_list = []
    cc = 0
    reader = csv.DictReader(csv_reader)
    for row in reader:
        try:
            generate_recommend_for_shop(row['name'], row['category'], row['city'])
            cc += 1
            print("%d.....%s"%(cc, row['name']))
        except Exception as e:
            print(e)

#f = open("cloudbd_shops_test_detail_one.csv", "r")
#generate_recommend_for_shop_by_full_info(f.read())

#f = open("cloudbd_comment.csv", "r")
#extract_keyword_from_comment(f.read())
