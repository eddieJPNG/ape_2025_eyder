#UMA FUNÇÃO QUE CALCULA A PORCENTAGEM DE UM NÚMERO POR OUTRO:

number_porcent = int(input("Digite um número como porcentagem: "))
number_alt = int(input("Digite um número para ser alterado: "))

def porcentagem(num1, num2):
    return num1 * num2 / 100


print(porcentagem(number_porcent, number_alt))

