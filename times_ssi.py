import timeit, time
import functions, values
import pandas as pd

list_emission = []
list_verification = []
emission_time = verification_time = ""

def calculate_times():
    global emission_time, verification_time
    values.fill_values()

    # Tempo de Emissao de uma VC no VDR pelo emissor

    begin_1 = timeit.default_timer()
    functions.issue_vc(1)
    end_1 = timeit.default_timer()
    time_1 = ((end_1 - begin_1) * 1000000)
    emission_time = ("Duração Emissao VC: %f ms" % time_1)
    print(emission_time)
    list_emission.append(time_1)

    # Tempo de Verificacao de uma VC no VDR pelo verificador

    begin_2 = timeit.default_timer()
    functions.verify_vc("Test", 1)
    end_2 = timeit.default_timer()
    time_2 = ((end_2 - begin_2) * 1000000)
    verification_time = ("Duração Verificacao VC: %f ms" % time_2)
    print(verification_time)
    list_verification.append(time_2)

def create_df():
    data = {
        'Emission_VC': list_emission,
        'Verification_VC': list_verification
    }

    df = pd.DataFrame(data)
    df.to_csv('report_ssi.csv', index=False)

def data_analysis():
    df = pd.read_csv('report_ssi.csv')
    #print(df.describe())
    media = df.mean()
    print("Média dos valores: \n", media)

    mediana = df.median()
    print("Mediana dos valores: \n", mediana)

    moda = df.mode()
    print("Moda dos valores: \n", moda)    

def main_ssi(replications):
    global emission_time, verification_time
    # Numero de replicacoes
    n = replications

    # Zera report atual
    with open('report_ssi.txt', 'w') as f:
        f.write("")

    # Executa replicacoes
    for i in range(n):
        replication = "=== Replicação %d ===" % (i+1)
        print(replication)
        calculate_times()

        with open('report_ssi.txt', 'a') as f:
            f.write(replication + "\n")
            f.write(emission_time + "\n")
            f.write(verification_time + "\n")
            f.write("\n \n")

    # Encontra valores minimo e maximo das replicacoes
    max_emission, min_emission = max(list_emission), min(list_emission)
    max_verification, min_verification = max(list_verification), min(list_verification)


    create_df()
    data_analysis()

    print("== Resultados: ==")
    max_min_emission = ("Mínimo e Máximo Emission VC: [%f ms; %f ms]" % (min_emission, max_emission))
    print(max_min_emission)
    max_min_verification = ("Mínimo e Máximo Verification VC: [%f ms; %f ms]" % (min_verification, max_verification))
    print(max_min_verification)

    with open('report_ssi.txt', 'a') as f:
        f.write("== Resultados: ==" + "\n")
        f.write(max_min_emission + "\n")
        f.write(max_min_verification + "\n")
        f.write("\n \n")


