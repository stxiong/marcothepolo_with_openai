import pymongo

mongo_cli = pymongo.MongoClient("localhost", 27017)
product_db = mongo_cli['1688_product']
product_table = product_db['gpt_product_info_20230227']
product_table.create_index([('item_id', pymongo.ASCENDING)], unique=True)


term_dict = {}

def clean_term(term):
    term = term.strip().lower()
    return term


def parse_line(line):
    terms = line.split(':')
    if len(terms) == 2:
        terms[0] = clean_term(terms[0])
        terms[1] = clean_term(terms[1])
        if terms[0] not in term_dict:
            term_dict[terms[0]] = {
                'values': {},
                'tot_count': 0
            } 
        if terms[1] not in term_dict[terms[0]]['values']:
            term_dict[terms[0]]['values'][terms[1]] = 0
        term_dict[terms[0]]['values'][terms[1]] += 1
        term_dict[terms[0]]['tot_count'] += 1
    else:
        print(line)

def parse_doc(doc):
    item_specifies = doc['gpt_content']['item_specifies'].split('\n')
    for item_line in item_specifies:
        parse_line(item_line)

doc_count = 0
for doc in product_table.find():
    parse_doc(doc)
    doc_count += 1


for k, v in sorted(term_dict.items(), key=lambda item: item[1]['tot_count']):
    print("%s,%s"%(k,v))

print("%d docs processed..."%doc_count)
