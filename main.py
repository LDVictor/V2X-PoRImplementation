import times_por, times_v2x, times_ssi

replications = 10

def op1():
    times_por.main_por(replications)

def op2():
    times_v2x.main_v2x(replications)

def op3():
    times_ssi.main_ssi(replications)

def main():
    global replications
    print("V2X Times Implementation")
    print("\n\n")
    replications = int(input("Insira o numero de replicacoes:"))
    while True:
        print("\n\n")
        print("Selecione uma das opcoes abaixo:")
        print("1 - Proof of Reputation")
        print("2 - V2X Communication")
        print("3 - SSI VC Emission & Verification")
        print("0 - Sair")
        opcao = int(input())
        if (opcao == 1):
            op1()
        elif (opcao == 2):
            op2()
        elif (opcao == 3):
            op3()
        elif (opcao == 0):
            break
        else:
            print("Opcao Invalida.")

main()