import os
import openai

openai.api_key = "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"

#prompt = "this is specific for a clothes product in key-value format, please help to translate to english: 主面料成分的含量:100"
#prompt = "this is specific for a clothes product in key-value format,  please help to translate to english: 主面料成分的含量:100."
#prompt = "I am the owner of the following store, neko stop, 102 Japanese Village Plaza Mall, CA 90012. I searched “Molly” on a wholesale website to find products I want to resell. Answer the question directly as bulletpoints and in short. What is the demographics of my target audience based on my store name and location? List Age, and Income and why you guess so.  Based on the demographics, what other keywords and corresponding price ranges do you recommend me search for something to sell, and why for each? List five. "
prompt = "I am the owner of the following store, neko stop, 102 Japanese Village Plaza Mall, CA 90012. I searched “Molly” on a wholesale website to find products I want to resell. Answer the question directly as bulletpoints and in short. What is the demographics of my target audience based on my store name and location? List Age, and Income and why you guess so.  Based on the demographics, what other keywords and corresponding price ranges do you recommend me search for something to sell, and why for each? List five."

#response = openai.Completion.create(
#  model="text-davinci-003",
##  model="gpt-4",
#  prompt=prompt,
#  max_tokens=1024,
#  temperature=0.2,
#  frequency_penalty=0.0,
#  presence_penalty=0.0
#)


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
#    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant for small merchant."},
        {"role": "user", "content": "I am the owner of the following store, noisy store, nanshan district, Shenzhen. I searched “mask” on a wholesale website to find products I want to resell. Answer the question directly as bulletpoints and in short. What is the demographics of my target audience based on my store name and location? List Age, and Income and why you guess so.  Based on the demographics, what other keywords and corresponding price ranges do you recommend me search for something to sell, and why for each? List five. And please response in Chinese"}
    ]
)

#print(response.choices[0]['text'].strip())
print(response.choices[0]["message"]["content"].strip())
print(response.choices)
print(response.usage)


