import csv
import os
import openai
import time
import datetime

#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"


def parse_product(id, title, body_html):
    print(id)
    prompt="please remove all the html tags for this text: %s"%body_html
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      max_tokens=300,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    #print (response.choices[0]['text'])
    #print ('------------------------')
    
    body_content = response.choices[0]['text']
    prompt = "this is some information of a product, please help to genenrate a product title make it like Amazon bestseller product: %s %s"%(body_content, title)
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
    return gpt_title


timestamp_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
with open('20230129170415386.csv', newline='') as csv_reader:
    with open('result_by_gpt_20230129170415386_%s.csv'%timestamp_str, 'w', newline='') as csv_writer:
        writer_fieldnames = ['id', 'original_title', 'title_by_gpt']
        writer = csv.DictWriter(csv_writer, fieldnames=writer_fieldnames)
        writer.writeheader()
        
        reader = csv.DictReader(csv_reader)
        for row in reader:
            try:
                gpt_title = parse_product(row['id'], row['title'], row['body_html'])
                writer.writerow({
                    'id': row['id'],
                    'original_title': row['title'],
                    'title_by_gpt': gpt_title
                })
                time.sleep(2)
                #break
            except Exception as e:
                print(e)
csv_reader.close()
csv_writer.close()
