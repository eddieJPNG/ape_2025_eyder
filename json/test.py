text_cases = int(input())

def validate_ra(ra):
    if len(ra) != 20:
        return False
    if not ra.startswith('RA'):
        return False
    if not ra[2:].isdigit():
        return False

# strf = 'Hey'.startswith('H')



while text_cases > 0:
    text_cases -= 1

    ra = input().strip()

l = ['hey', 'hello', 'hi', 'greetings', 'salutations']

print(enumerate(l))