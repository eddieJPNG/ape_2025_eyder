import json

def pr(var):
    print(var)

# json_file = '["a": 12, "b": "hey", c: True]'

# data = json.load(json_file)

# print(data)

a = 10
b = 45.7
c = "Hey"
d = ['hey', 20, None, True, 2.3]
e = {
    'int': 6,
    'string': 'hey',


}

print(json.dumps(e))

fu = json.loads('"hey"')
# print(type(f))

f = open('teste.json', 'rt')

print(f)

f_read = f.read()

print(f_read)

j = json.loads(f_read)

print(j)

pr(j = "hey")