# def oi():
#     print('oi')
    
#     return

# oi()

# print(bin(64000009))

# x = bin(64000009)
# print(x)
# print(x.count('1'))

#VALORES DEFAULT PARA FUNCOES


def dados(name='nome', age=18, height=1.80):
    print(f'Nome: {name}, Idade: {age}, Altura: {height}')

dados('Eddie', 20, 1.75)

def soma(a,b):
    c = a + b
    return c
    

soma = soma(2,3)
print(soma)

def avg(values):
    if not isinstance(values, (list, tuple)):
        return 0.0
    
    if isinstance(values, (int, float)):
        return values
    
    count = len(values)
    if count == 0:
        return 0.0

    sum = 0.0
    for value in values:
        sum += value # sum = sum + value
    return sum / len(values)

print(avg([1,4,50]))
print(avg((2,45,22)))
print(avg(20))
print(avg(2.666))
print(avg(5.01))

def avg2(*values):
    return print(type(values), values)

#O "*" transforma os argumentos em uma tupla

print(avg2(12,45,67))

#isinstance

#FERRAMENTA MUITO PODEROSA!


#NOS PARAMETROS DA FUNCOES UM "*" ANTES DO PARAMETRO TRANSFORMA OS ARGUMENTOS EM UMA TUPLA, IDEPENDENTEMENTE DA SITUAÇÃO É O DIABO DE UMA TUPLA.

# Grupo dos bonecos: 8 horas;
# Grupo dos arquitetos: 4 horas;
# Grupo dos musicos: 6 horas;
# Grupo dos desenhistas: 12 horas.

# Aradhel bonecos 10 - 1
# Aerin arquitetos 15 - 3
# Anna musicos 10 - 1
# Elbereth musicos 10 - 1
# Freda desenhistas 15 - 1
# Arwen bonecos 10 - 1
# Logolas bonecos 10 - 1

print(1+3+1+1+1+1+1)

print("===============================================================")
print("===============================================================")
print("===============================================================")


#key words arguments 


def func(a, b, c):
    print(a, b, c)

func(2,4,66)

func(b=55, c=99, a=61)

def dic(a,b,**f):
    print(a,b)
    print(f)

#PARAMETROS COMO "**F" NÃO SAO OBRIGATORIOS

def dic2(**ficha):
    return ficha.copy

ficha = dic2(nome="Baki", altura="1.60", estilo="misto")


print(
    bin(-28330)
)

print("===============================================================")
print("===============================================================")
print("===============================================================")


eddie = {1,2}

print(eddie)

#AQUELE QUESITO DAS VARIAVEIS ARMAZENADAS NA MEMORIA SE APLICAM SEMELHANTEMENTE A FUNÇÕES.

print("===============================================================")
print("===============================================================")
print("===============================================================")


def calc(a,b,operation):
    return operation(a,b)

def add(a,b):
    return a + b

def mul(a,b):
    return a * b

def sub(a,b):
    return a - b

def div(a,b):
    return a / b

print(add(1,2))
print(mul(1,2))
print(sub(1,2))
print(div(1,2))
print(calc(1,2, add))
print(calc(1,2, mul))
print(calc(1,2, sub))
print(calc(1,2, div))

print("===============================================================")
print("===============================================================")
print("===============================================================")


import random

print(random.randint(1, 20))
print(random.randint(1, 20))
print(random.randint(1, 20))
print(random.randint(1, 20))
print(random.randint(1, 20))
print(random.randint(1, 20))
print(random.randint(1, 20))


print("===============================================================")
print("===============================================================")
print("===============================================================")

#FACA UMA FUNC DE RANDOM_NUMBER(), DEPOIS FACA UMA C/10 NUMEROS COM UMA 
#QUANTIDADE ALEATÓRIA DE DIGITOS (1 A 5), E ORDENE PELA QUNAITDADE DE DIGITOS.



def random_number(n):
    listb = []


    for i in range(n+1):
        listb.append(i)

    print(listb)

print(random_number(7))

print(564 % 2)

print("===============================================================")
print("===============================================================")
print("===============================================================")
