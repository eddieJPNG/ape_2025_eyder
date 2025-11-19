import re

regex = r"^[+-]?\d+/[+=]?\d+$"

print(re.match(regex, "-6/2"))
print(re.match(regex, "n76/2"))


print("Maria\nJoao")
print(r"Maria\nJoao")

