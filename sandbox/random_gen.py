import random
import string

def gerar_senha(tamanho=12, incluir_simbolos=True):
    """
    Gera uma senha aleatória com o tamanho e opções definidos.
    """
    caracteres = string.ascii_letters + string.digits
    if incluir_simbolos:
        caracteres += string.punctuation
    
    senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return senha


def exibir_boas_vindas():
    """
    Exibe uma mensagem de introdução ao programa.
    """
    print("=" * 40)
    print("🔐 GERADOR DE SENHAS ALEATÓRIAS 🔐")
    print("=" * 40)


def menu():
    """
    Mostra o menu e solicita opções ao usuário.
    """
    while True:

        exibir_boas_vindas()
        try:
            tamanho = int(input("Digite o tamanho da senha desejada: "))
            incluir = input("Deseja incluir símbolos? (s/n): ").strip().lower() == 's'
            
            senha = gerar_senha(tamanho, incluir)
            print(f"\nSua senha gerada é: {senha}")
        except ValueError:
            print("\n⚠️ Valor inválido! Digite um número inteiro para o tamanho.")
        finally:
            print("\nPrograma finalizado.\n")


# --- Ponto de entrada do script ---
if __name__ == "__main__":
    menu()
