import json

obj = {}
obj['f1'] = 1
obj['f2'] = 2

s = json.dumps(obj)

obj2 = json.loads(s)

print(obj2)