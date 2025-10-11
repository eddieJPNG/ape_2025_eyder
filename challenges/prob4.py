# 4. Primeira Letra de Cada Palavra
# Receba uma frase e imprima apenas a **primeira letra de cada palavra**, todas juntas sem espaços.
# **Entrada exemplo:**
# ```
# Maratona de Programacao
# print(char)

phrase = input("Digite uma frase: ")

firsts_words = []

for char in phrase.split():
    firsts_words.append(char[0])
    
   # .upper()

print("".join(firsts_words))

    