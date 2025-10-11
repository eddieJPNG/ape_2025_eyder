def write(*args, s="-"):
    print(args, sep=s)

write("oi")

args = (1,2,3)

write(*args)
print("====================================================================")
write(args)
print("====================================================================")
write("hello", "world")