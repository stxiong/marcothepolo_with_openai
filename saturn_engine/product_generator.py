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
        
    def __generate_basic_product_context(self, language='English'):
        
        prompt = 'this is some information of a product in strict json format: [%s],'%json.dumps(self.item_specifics)
        prompt += 'and the item name in Chinese is: [%s]. \n'%self.item_name
        prompt += ' help to generate one product title for this item no more than 35 words,'
        prompt += ' and generate one short title for this item with no more than 45 charactors, '
        prompt += ' and also generate a recomend text for online selling with at less 5 sentences, ' 
        prompt += ' and extract no more than 10 most important tags for describing this online product in %s.'%language 
        prompt += ' the output must be in strict JSON format: "short title": "the title you generate", "product title": "the title you generate", "recommend": "the recommend text you generate", "tags": "[important tags array you selected]". ' 
        prompt += ' the language of all the output values must be only %s, '%language
        prompt += ' and please notice that do not include any information about cross-border.'
        
        print(prompt)
        openai.api_key = self.OPENAI_KEY
        response = openai.Completion.create(
          model=self.DEFAULT_OPENAI_COMPLETION_MODEL,
          prompt=prompt,
          max_tokens=2056,
          temperature=0.6,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )

        result = {
            'context': response.choices[0]['text'],
            'usage': response.usage
        }
        return result
    

    def run(self, language='English'):
        result = self.__generate_basic_product_context(language)

        return result

    
