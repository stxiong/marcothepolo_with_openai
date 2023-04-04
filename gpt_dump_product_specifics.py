import pymongo

mongo_cli = pymongo.MongoClient("localhost", 27017)
product_db = mongo_cli['1688_product']
product_table = product_db['gpt_product_info_20230315']
product_table.create_index([('item_id', pymongo.ASCENDING)], unique=True)


term_dict = {}

def clean_term(term):
    term = term.strip().lower()
    term = term.replace('\n', ' ')
    return term


def parse_line(item_id, line):
    input_key = line['input-key']
    input_value = line['input-value']
    output = clean_term(line['output'])
    
    if input_key not in term_dict:
        term_dict[input_key] = {}
    if input_value not in term_dict[input_key]:
        term_dict[input_key][input_value] = {}
    if output not in term_dict[input_key][input_value]:
        term_dict[input_key][input_value][output] = {
            'count': 0,
            'item_id': item_id 
        }
    term_dict[input_key][input_value][output]['count'] += 1 
        

def parse_doc(doc):
    item_specifies = doc['gpt_content']['translated_item_specifics']
    item_id = doc['item_id']
    for item_line in item_specifies:
        parse_line(item_id, item_line)

doc_count = 0
for doc in product_table.find():
    parse_doc(doc)
    doc_count += 1


#for k, v in sorted(term_dict.items(), key=lambda item: item[1]['tot_count']):
#    print("%s,%s"%(k,v))

for input_key, v in term_dict.items():
    for input_value, vv in v.items():
        for output, stat in vv.items():
            print("\"%s\",\"%s\",\"%s\",\"%d\",\"%s\""%(input_key, input_value, output, stat['count'], stat['item_id']))

print("%d docs processed..."%doc_count)
