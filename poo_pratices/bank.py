class ContaBancaria:
    def __init__(self, titular):
        self.titular = titular
        self.saldo = 0.0

    def depositar(self, valor):
        self.saldo += valor

    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
        else:
            print("Saldo insuficiente!")

    def ver_saldo(self):
        print(f"{self.titular}, seu saldo é R${self.saldo:.2f}")

conta = ContaBancaria("Edson")
conta.depositar(1000)
conta.sacar(250)
conta.ver_saldo()

conta1 = ContaBancaria("José Raimudo da Silva")
conta1.depositar(1200)
conta1.ver_saldo()
conta1.sacar(560)
conta1.ver_saldo()

