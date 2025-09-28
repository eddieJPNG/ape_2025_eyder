# ## 2. Palíndromo Simples

# Leia uma string e verifique se ela é um palíndromo (igual lida de frente para trás e de trás para frente). Escreva "SIM" se for, ou "NAO" caso contrário.

# **Entrada exemplo:**

# ```
# arara
# ```


palindrome = input()

reverse_text = palindrome[: : -1]

print(reverse_text)

if palindrome == reverse_text:
    print(f"{palindrome} é um palíndromo")
else:
    print(f"{palindrome} não é um palíndromo")

    
