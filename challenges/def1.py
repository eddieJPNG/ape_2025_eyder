#1. Contagem de Vogais
#Dada uma string, conte quantas vogais (a, e, i, o, u) existem nela. A saída deve ser apenas um número inteiro.
#
#programacao
   

text = input()
counter = 0
vowels = 'aeiou'
vowels = list(vowels)

for i in text:
    if i in vowels:
        counter += 1

print(counter)