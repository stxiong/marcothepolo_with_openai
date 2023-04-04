from saturn_engine import ProductContextGenerator


openai_key = "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"
origin_data_file = "1688_test.json"
with open(origin_data_file, "r") as file_in:
    for line in file_in.readlines():
        obj = ProductContextGenerator(line, openai_key)
        result = obj.run()
        print(result)
