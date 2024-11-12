# coding: utf-8
import timeit, time
import functions, values
import pandas as pd

## Script Principal

replication = ""

list_trust_rep = []
list_sw = []
list_tpor = []
list_dpor = []
list_fpor = []
list_ic = []
list_trust_ic = []

def calculate_times():

    # Ajuste de atraso (delay) entre medicoes
    delay = 0

    global replication
    values.fill_values()

    # Tempo de Calculo da Funcao Trust Rep

    begin_1 = timeit.default_timer()
    functions.return_trust_rep(values.rep)
    end_1 = timeit.default_timer()
    time_1 = ((end_1 - begin_1) * 1000)
    trust_rep_time = ("Duração TRUST_REP: %f ms" % time_1)
    print(trust_rep_time)
    list_trust_rep.append(time_1)

    time.sleep(delay)

    # Tempo de Calculo da Funcao SW

    begin_2 = timeit.default_timer()
    functions.verify_sw(values.t_v, values.timestamp)
    end_2 = timeit.default_timer()
    time_2 = ((end_2 - begin_2) * 1000)
    sw_time = ("Duração SW: %f ms" % time_2)
    print(sw_time)
    list_sw.append(time_2)

    time.sleep(delay)

    # Tempo de Calculo da Funcao Tpor

    begin_3 = timeit.default_timer()
    t_por = functions.calculate_tpor(values.t_approx, values.t_current)
    end_3 = timeit.default_timer()
    time_3 = ((end_3 - begin_3) * 1000)
    tpor_time = ("Duração TPOR: %f ms" % time_3)
    print(tpor_time)
    list_tpor.append(time_3)

    time.sleep(delay)

    # Tempo de Calculo da Funcao Dpor

    begin_4 = timeit.default_timer()
    d_por = functions.calculate_dpor(values.d_approx, values.d_ran)
    end_4 = timeit.default_timer()
    time_4 = ((end_4 - begin_4) * 1000)
    dpor_time = ("Duração DPOR: %f ms" % time_4)
    print(dpor_time)
    list_dpor.append(time_4)

    time.sleep(delay)

    # Tempo de Calculo da Funcao Fpor

    begin_5 = timeit.default_timer()
    functions.calculate_fpor(t_por, d_por)
    end_5 = timeit.default_timer()
    time_5 = ((end_5 - begin_5) * 1000)
    fpor_time = ("Duração FPOR: %f ms" % time_5)
    print(fpor_time)
    list_fpor.append(time_5)

    time.sleep(delay)

    # Tempo de Calculo da Funcao IC

    begin_6 = timeit.default_timer()
    ic = functions.calculate_ic(values.c_s, values.fpor_s)
    end_6 = timeit.default_timer()
    time_6 = ((end_6 - begin_6) * 1000)
    ic_time = ("Duração IC: %f ms" % time_6)
    print(ic_time)
    list_ic.append(time_6)

    time.sleep(delay)

    # Tempo de Calculo da Funcao Trust IC

    begin_7 = timeit.default_timer()
    functions.return_trust_ic(ic)
    end_7 = timeit.default_timer()
    time_7 = ((end_7 - begin_7) * 1000)
    trust_ic_time = ("Duração TRUST_IC: %f ms" % time_7)
    print(trust_ic_time)
    list_trust_ic.append(time_7)

def create_df():
    data = {
        'TRUST_REPs': list_trust_rep,
        'SWs': list_sw,
        'TPORs': list_tpor,
        'DPORs': list_dpor,
        'FPORs': list_fpor,
        'ICs': list_ic,
        'TRUST_ICs': list_trust_ic
    }

    df = pd.DataFrame(data)
    df.to_csv('report_por.csv', index=False)

def data_analysis():
    df = pd.read_csv('report_por.csv')
    #print(df.describe())
    media = df.mean()
    print("Média dos valores: \n", media)

    mediana = df.median()
    print("Mediana dos valores: \n", mediana)

    moda = df.mode()
    print("Moda dos valores: \n", moda)



def main_por(replications):
    # Numero de replicacoes
    n = replications

    # Zera report atual
    with open('report.txt', 'w') as f:
        f.write("")

    # Executa replicacoes
    for i in range(n):
        replication = "=== Replicação %d ===" % (i+1)
        print(replication)
        calculate_times()

        with open('report.txt', 'a') as f:
            f.write(replication + "\n")
            f.write(trust_rep_time + "\n")
            f.write(sw_time + "\n")
            f.write(tpor_time + "\n")
            f.write(dpor_time + "\n")
            f.write(fpor_time + "\n")
            f.write(ic_time + "\n")
            f.write(trust_ic_time + "\n")
            f.write("\n \n")

    # Encontra valores minimo e maximo das replicacoes
    max_trust_rep, min_trust_rep = max(list_trust_rep), min(list_trust_rep)
    max_sw, min_sw = max(list_sw), min(list_sw)
    max_tpor, min_tpor = max(list_tpor), min(list_tpor)
    max_dpor, min_dpor = max(list_dpor), min(list_dpor)
    max_fpor, min_fpor = max(list_fpor), min(list_fpor)
    max_ic, min_ic = max(list_ic), min(list_ic)
    max_trust_ic, min_trust_ic = max(list_trust_ic), min(list_trust_ic)

    create_df()
    data_analysis()

    print("== Resultados: ==")
    max_min_trust_rep = ("Mínimo e Máximo TRUST_REP: [%f ms; %f ms]" % (min_trust_rep, max_trust_rep))
    print(max_min_trust_rep)
    max_min_sw = ("Mínimo e Máximo SW: [%f ms; %f ms]" % (min_sw, max_sw))
    print(max_min_sw)
    max_min_tpor = ("Mínimo e Máximo TPOR: [%f ms; %f ms]" % (min_tpor, max_tpor))
    print(max_min_tpor)
    max_min_dpor = ("Mínimo e Máximo DPOR: [%f ms; %f ms]" % (min_dpor, max_dpor))
    print(max_min_dpor)
    max_min_fpor = ("Mínimo e Máximo FPOR: [%f ms; %f ms]" % (min_fpor, max_fpor))
    print(max_min_fpor)
    max_min_ic = ("Mínimo e Máximo IC: [%f ms; %f ms]" % (min_ic, max_ic))
    print(max_min_ic)
    max_min_trust_ic = ("Mínimo e Máximo TRUST_IC: [%f ms; %f ms]" % (min_trust_ic, max_trust_ic))
    print(max_min_trust_ic)

    with open('report.txt', 'a') as f:
        f.write("== Resultados: ==" + "\n")
        f.write(max_min_trust_rep + "\n")
        f.write(max_min_sw + "\n")
        f.write(max_min_tpor + "\n")
        f.write(max_min_dpor + "\n")
        f.write(max_min_fpor + "\n")
        f.write(max_min_ic + "\n")
        f.write(max_min_trust_ic + "\n")
        f.write("\n \n")
