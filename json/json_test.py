with open('test.txt', 'r') as archive:
    view = archive.read()

print(view)

print("=" * 10)

with open('test.txt', 'r') as archive:
    for k in archive:
        print(k.strip())

with open('test.txt', 'r') as archive:
    view2 = archive.read(10)

print("=" * 10)


print(view2)

with open('test.txt', 'w') as archive:
    text = 'Substitui os jojos'
    write0 = archive.write(text)
    print("=" * 10)
    print(write0)

with open('test.txt', 'a') as archive:
    view3 = archive.write('Johanna')
    view4 = archive.read()
    print("=" * 10)

    print(view4)
