#SORTEAR 3 LETRAS DO ALFABETO E FORMAR UMA PALAVRA COM ELAS:

import random

num_words = int(input("Com quantas letras você quer formar a palavra?: "))

alpha = 'abcdefghijklmnopqrstuvwxyz'
wolwes = 'aeiou'

random_word = []


while num_words > 0:
    num_words -= 1
    
    random_word.append(alpha[random.randint(0,25)])
    
    

print("Palavra formada:", "".join(random_word))

counter = 0

for i in random_word:
   
    if i in wolwes:
        continue
    else:
        counter += 1

    if counter == len(random_word):
        random_word.append(wolwes[random.randint(0,4)])
        print("Palavra com vogal:" ,"".join(random_word))
        
        
