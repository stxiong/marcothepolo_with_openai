import os
import openai

openai.api_key = "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"

prompt = "I am the owner of the following store, neko stop, 102 Japanese Village Plaza Mall, CA 90012.I searched “Molly” on a wholesale website to find products I want to resell. Answer the question directly as bulletpoints and in short.What is the demographics of my target audience based on my store name and location? List Age, and Income and why you guess so. Based on the demographics, what other keywords and corresponding price ranges do you recommend me search for something to sell, and why for each? List five."

response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  max_tokens=1024,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)

print(response.choices[0]['text'].strip())
print(response.choices)
print(response.usage)


