plus_ten = lambda e: e + 10

print(plus_ten(5))

lambtest = lambda stringer: stringer.upper()

print(lambtest("text"))

sic = [
{"a": "oi", "b": 5,},
{"c": 8, "d": "Hey",},
]

print("1", sic[0])
print("2", sic[1])
print("3", sic[0].keys())
print("4", sic[0].values())
print("5", sic[0].keys())

searcher = 6
counter = 0

for keys in sic[0].keys():
    
    counter += 1

    print(f"{counter}º {keys}")

