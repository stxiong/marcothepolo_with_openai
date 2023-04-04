import json

a = '{"1": "1", "2": 2"}'

b = json.loads(a)
print(b.keys())
