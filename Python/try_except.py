
print("===================INICIO=========================")

try:

    number = int(input("digite um número: "))

    result = 10/number

    print("resultado: %.2f" % result)

except ZeroDivisionError as error:
    print("Erro: não é possível dividir por 0")
    print("Erro:", error) 
except ValueError:
    print("Erro: Entrada não válida")
    
print("=====================FIM========================")

