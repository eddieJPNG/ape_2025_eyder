from math import sqrt, floor 

def prime(n):
    max = floor(sqrt(n))
    for div in range(2, max + 1):
        if n % div == 0:
            return False #se não entar nesse if, n é um primo certeza
        return True



print('### verifica se o inteiro é primo ###\n')
number = int(input('Digite um inteiro: '))

if prime(number) == True:
    print(f'{number}, é primo!')
else:
    print(f'{number}, não é primo!')

prime(number)

print(f'### GERA TODOS OS PRIMOS ENTRE 1 E {number} ###\n')

# primes = [srt(w) for w in range(1, number + 1) if prime(w)]

# print(' ,'.join(primes))

#generators
print('---------------------------------------------------------------')
x = ( x * 3 for x in range(1,11))
print(list(x))

d = {}

for k in 'abcdefghijklmnopqrstuvwxyz':
    d[k] = 0

print(d)


print('=====================================================')


