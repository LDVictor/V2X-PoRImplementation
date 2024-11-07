import timeit, time
import functions, values
import pandas as pd

list_v2v = []
list_v2n = []
v2v_time = v2n_time = ""

def calculate_times():
    global v2v_time, v2n_time
    values.fill_values()

    # Tempo de Transmissao de uma mensagem V2V

    begin_1 = timeit.default_timer()
    functions.send_v2v_msg("ADAS info - Highway X: Heavy Traffic")
    end_1 = timeit.default_timer()
    time_1 = ((end_1 - begin_1) * 1000)
    v2v_time = ("Duração V2V Msg: %f ms" % time_1)
    print(v2v_time)
    list_v2v.append(time_1)

    # Tempo de Transmissao de uma mensagem V2N
    begin_2 = timeit.default_timer()
    functions.send_v2n_msg("ADAS info - Highway X: Heavy Traffic")
    end_2 = timeit.default_timer()
    time_2 = ((end_2 - begin_2) * 1000)
    v2n_time = ("Duração V2N Msg: %f ms" % time_2)
    print(v2n_time)
    list_v2n.append(time_2)

def create_df():
    data = {
        'V2V': list_v2v,
        'V2N': list_v2n
    }

    df = pd.DataFrame(data)
    df.to_csv('report_v2x.csv', index=False)

def data_analysis():
    df = pd.read_csv('report_v2x.csv')
    #print(df.describe())
    media = df.mean()
    print("Média dos valores: \n", media)

    mediana = df.median()
    print("Mediana dos valores: \n", mediana)

    moda = df.mode()
    print("Moda dos valores: \n", moda)

def main_v2x(replications):
    global v2v_time, v2n_time
    # Numero de replicacoes
    n = replications

    # Zera report atual
    with open('report_v2x.txt', 'w') as f:
        f.write("")

    # Executa replicacoes
    for i in range(n):
        replication = "=== Replicação %d ===" % (i+1)
        print(replication)
        calculate_times()

        with open('report_v2x.txt', 'a') as f:
            f.write(replication + "\n")
            f.write(v2v_time + "\n")
            f.write(v2n_time + "\n")
            f.write("\n \n")

    # Encontra valores minimo e maximo das replicacoes
    max_v2v, min_v2v = max(list_v2v), min(list_v2v)
    max_v2n, min_v2n = max(list_v2n), min(list_v2n)


    create_df()
    data_analysis()

    print("== Resultados: ==")
    max_min_v2v = ("Mínimo e Máximo V2V: [%f ms; %f ms]" % (min_v2v, max_v2v))
    print(max_min_v2v)
    max_min_v2n = ("Mínimo e Máximo V2N: [%f ms; %f ms]" % (min_v2n, max_v2n))
    print(max_min_v2n)

    with open('report_v2x.txt', 'a') as f:
        f.write("== Resultados: ==" + "\n")
        f.write(max_min_v2v + "\n")
        f.write(max_min_v2n + "\n")
        f.write("\n \n")








