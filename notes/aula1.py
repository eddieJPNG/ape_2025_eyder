import math
from math import sqrt
from math import floor
from random import randint
from .aula2 import greet_user

#COMPREHENSIONS

# [expression for item in interable if condition]

squares = [i ** 2 for i in range(1,6)]

print(squares)

#MESMO QUE:

squares2 = []

for i in range(1,6):
    squares2.append(i ** 2)

print(squares2)

mul3 = [i for i in range(3, 101, 3)]

print(mul3)

# print(list(range(3, 101, 3)))

#RANGE TERCEIRO PARAMETRO É O PASSO, DE QUAUNTO ELE VAI DE X  EM X.

#ATIVIDADE DOS NÚMEROS PRIMOS
#W É PRIMO SE K/W:
#INETREVALO DE 1 < K <= RAIZ-QUADRADA(W)
#W = NÚMERO DO PARAMETRO NA FUNCAO


def prime(n):
    max = floor(sqrt(n))
    for div in range(2, max + 1):
        if n % div == 0:
            return False #se não entar nesse if, n é um primo certeza
        return True

prime(100)

print(sqrt(100))

print(math.pi)

#DIC E SET COMPREHESNION

zz = randint(1,6)

print(zz)

r = ( randint(0,10) for x in range(10))
print(r)

print(tuple(r))
print()

#SET E ESSES ACIMA PESQUISAR.