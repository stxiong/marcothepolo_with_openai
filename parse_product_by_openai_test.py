import os
import openai

openai.api_key = "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"

store_name = "Zara"
location = "south figueroa street space 301 725, Los Angeles, CA 90017"
keywords = "hats" 

#prompt = "I am the owner of the following store, Phil's Discount Store, 1451 1/2 W 3rd St, Los Angeles, CA 90017. I searched “cable” on a wholesale website to find products I want to resell. Answer the question directly as bulletpoints and in short. What is the demographics of my target audience based on my store name and location? List Age, and Income and must tell me the reasoning in detail. Based on the demographics, what other keywords and corresponding price ranges do you recommend me search for something to sell, and why for each? List five."
prompt = "I am the owner of the following store, %s , \
    %s. \
    I searched “%s” on a wholesale website to find products for resell. \
    Answer the question directly as bulletpoints and in short.Based on my store name and demographics of the surrounding are of store location, What is the demographics of my target audience List Age, Income, and another important feature. Explain why you guess so. Based on the demographics, what keywords and corresponding price range should I refine my search to narrow down my purchases, and why for each? List five.Based on the demographics, what keywords in other categories and corresponding price ranges should I search, \
    and why for each? List five."%(store_name, location, keywords)

response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  max_tokens=1024,
  temperature=0.2,
#  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)

print(response.choices[0]['text'].strip())
print(response.choices)
print(response.usage)


