import json
import openai

class ProductContextGenerator(object):
      
    @staticmethod
    def parse_specific_dict(item_specifics):
        result = {}
        for kv in item_specifics:
            result[kv['name']] = kv['value']
        return result
    
    DEFAULT_OPENAI_COMPLETION_MODEL = "text-davinci-003" 
    OPENAI_KEY = None
    product_info_dict = {}
    item_id = None
    item_name = None
    item_specifics = None   
    category = None

    def __init__(self, product_json, openai_key, source='1688', category=None):
        self.OPENAI_KEY = openai_key
        self.product_info_dict = json.loads(product_json)
        self.item_id = self.product_info_dict['item_id']
        self.item_name = self.product_info_dict['item_name']
        self.item_specifics = ProductContextGenerator.parse_specific_dict(self.product_info_dict['item_specifics'])
        self.category = None
        
    def __generate_title(self, max_tokens, temperature, language='English'):
        
        prompt = "this is some information of a product in json format,"
        if self.category != None:
            prompt += " and this is a %s product"%self.category 
        prompt += " please help to genenrate a product title in english," 
        prompt += " the title should only include %s words,"%language
        prompt += " and please notice that don't include any information about 'cross-border'"
        prompt += " : %s %s."%(self.item_name, json.dumps(self.item_specifics))
        
        openai.api_key = self.OPENAI_KEY
        response = openai.Completion.create(
          model=self.DEFAULT_OPENAI_COMPLETION_MODEL,
          prompt=prompt,
          max_tokens=max_tokens,
          temperature=temperature,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
        result = {
            'title': response.choices[0]['text'].strip(),
            'usage': response.usage
        }
        return result 
    
    
    def __generate_full_title(self, language='English'):
        result = self.__generate_title(
            max_tokens=64,
            temperature=1,
            language=language
        )
        return result
    
    def __generate_short_title(self, language='English'):
        result = self.__generate_title(
            max_tokens=16,
            temperature=0.6,
            language=language
        )
        return result   
            
    def __generate_important_tags(self, language='English'):
        prompt = "this is some information of a product in json format,"
        if self.category != None:
            prompt += " and this is a %s product;"%self.category
        prompt += " please extract no more than 10 most important tags for describing this online product," 
        prompt += " only in %s: %s."%(language, json.dumps(self.item_specifics))
        
        openai.api_key = self.OPENAI_KEY
        response = openai.Completion.create(
          model=self.DEFAULT_OPENAI_COMPLETION_MODEL,
          prompt=prompt,
          max_tokens=1024,
          temperature=0.2,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
        result = {
            'important_tags': response.choices[0]['text'],
            'usage': response.usage
        }
        return result
    
    def __generate_recommend_essay(self, language='English'):
        prompt = "this is some information of a product in json format,"
        if self.category != None:
            prompt += " and this is a %s product;"%self.category
        prompt += " please help to generate a short recomend text in %s"%language
        prompt += " for online selling: %s %s."%(self.item_name, json.dumps(self.item_specifics))
        
        openai.api_key = self.OPENAI_KEY
        response = openai.Completion.create(
          model=self.DEFAULT_OPENAI_COMPLETION_MODEL,
          prompt=prompt,
          max_tokens=256,
          temperature=0.6,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
        result = {
            'recommend_essay': response.choices[0]['text'],
            'usage': response.usage
        }
        return result
    
    
    def run(self, language='English'):
        result = {
            'usage': {
                'completion_tokens': 0,
                'prompt_tokens': 0,
                'total_tokens': 0 
            }
        }
        
        short_title_result = self.__generate_short_title()
        print(short_title_result)
        result['short_title'] = short_title_result['title']
        result['usage']['completion_tokens'] += short_title_result['usage']['completion_tokens']
        result['usage']['prompt_tokens'] += short_title_result['usage']['prompt_tokens']
        result['usage']['total_tokens'] += short_title_result['usage']['total_tokens']

        full_title_result = self.__generate_full_title()
        print(full_title_result)
        result['full_title'] = full_title_result['title']
        result['usage']['completion_tokens'] += full_title_result['usage']['completion_tokens']
        result['usage']['prompt_tokens'] += full_title_result['usage']['prompt_tokens']
        result['usage']['total_tokens'] += full_title_result['usage']['total_tokens']
    
        important_tags_result = self.__generate_important_tags()
        print(important_tags_result)
        result['important_tags'] = important_tags_result['important_tags']
        result['usage']['completion_tokens'] += important_tags_result['usage']['completion_tokens']
        result['usage']['prompt_tokens'] += important_tags_result['usage']['prompt_tokens']
        result['usage']['total_tokens'] += important_tags_result['usage']['total_tokens']
    
        recommend_essay_result = self.__generate_recommend_essay()
        print(recommend_essay_result)
        result['recommend_essay'] = recommend_essay_result['recommend_essay']
        result['usage']['completion_tokens'] += recommend_essay_result['usage']['completion_tokens']
        result['usage']['prompt_tokens'] += recommend_essay_result['usage']['prompt_tokens']
        result['usage']['total_tokens'] += recommend_essay_result['usage']['total_tokens']
        
        return result
    
