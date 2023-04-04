from saturn_engine import ProductContextGenerator


openai_key = "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"
origin_data_file = "1688_test.json"
with open(origin_data_file, "r") as file_in:
    for line in file_in.readlines():
        obj = ProductContextGenerator(line, openai_key)
        result = obj.run('English')
        print(result)
