import csv 
import pymongo

mongo_cli = pymongo.MongoClient("localhost", 27017)
product_db = mongo_cli['1688_product']
product_table = product_db['gpt_product_info_20230227']
product_table.create_index([('item_id', pymongo.ASCENDING)], unique=True)


with open('gpt_gen_product_titles.csv', 'w', newline='') as csv_writer:
    writer_fieldnames = ['item_id', 'supplier', 'original_title', 'short_title', 'long_title']
    writer = csv.DictWriter(csv_writer, fieldnames=writer_fieldnames)
    writer.writeheader()

    for doc in product_table.find():
        writer.writerow({
            'item_id': doc['item_id'],
            'supplier': doc['seller_name'],
            'original_title': doc['item_name'],
            'short_title': doc['gpt_content']['short_title'],
            'long_title': doc['gpt_content']['long_title'],
        })

csv_writer.close()
