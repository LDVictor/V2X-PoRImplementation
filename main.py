import tkinter as tk
from tkinter import messagebox
import times_por, times_v2x

replications = 10

def op1():
    global replications
    messagebox.showinfo("Times - Proof of Reputation", "Calculating times")
    replications = int(campo_entrada.get())
    times_por.main_por(replications)

def op2():
    messagebox.showinfo("Times - V2X Communication", "Calculating times")
    replications = int(campo_entrada.get())
    times_v2x.main_v2x(replications)

def op3():
    messagebox.showinfo("Times - SSI VC Emission & Verification", "Calculating times")

def quit():
    janela.quit()

janela = tk.Tk()
janela.title("V2X Times Implementation")
janela.geometry("400x300")
titulo = tk.Label(janela, text="Menu Principal", font=("Arial", 16))
titulo.pack(pady=10)

rotulo = tk.Label(janela, text="Número de Replicações:")
rotulo.pack(pady=5)

campo_entrada = tk.Entry(janela, width=30)
campo_entrada.pack(pady=5)

botao_opcao1 = tk.Button(janela, text="Proof of Reputation", width=30, command=op1)
botao_opcao1.pack(pady=5)

botao_opcao2 = tk.Button(janela, text="V2X Communication", width=30, command=op2)
botao_opcao2.pack(pady=5)

botao_opcao3 = tk.Button(janela, text="SSI VC Emission & Verification", width=30, command=op3)
botao_opcao3.pack(pady=5)

botao_sair = tk.Button(janela, text="Quit", width=20, command=quit)
botao_sair.pack(pady=10)

janela.mainloop()
