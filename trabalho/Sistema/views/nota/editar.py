# editarNota.py
import tkinter as tk
from tkinter import ttk, messagebox
import importlib.util, os, sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)



# ---------------- CARREGANDO AS CLASSES ---------------- #

def carregar_class(nome):
    caminho = os.path.join('Sistema', 'entidades', f'{nome}.py')
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, nome)

Nota = carregar_class("Nota")


# ---------------- JANELA ---------------- #

def janela_editar(id_nota, recarregar):
    win = tk.Toplevel()
    win.title("Editar Nota")
    win.geometry("320x260")

    row = Nota.ler("id=%s", (id_nota,))[0]

    tk.Label(win, text="Nota Trabalho").pack()
    nota_trabalho_entry = tk.Entry(win)
    nota_trabalho_entry.insert(0, row[4])
    nota_trabalho_entry.pack()

    tk.Label(win, text="Nota Prova").pack()
    nota_prova_entry = tk.Entry(win)
    nota_prova_entry.insert(0, row[5])
    nota_prova_entry.pack()


# ---------------- SALVANDO ---------------- #

    def salvar():
        try:
            trab = float(nota_trabalho_entry.get())
            prov = float(nota_prova_entry.get())
            if not (0 <= trab <= 5 and 0 <= prov <= 5):
                raise ValueError
        except:
            messagebox.showwarning("Erro", "Notas devem ser números entre 0 e 5")
            return

        n = Nota(*row[1:-1])  # remove id
        n.nota_trabalho = trab
        n.nota_prova = prov

        messagebox.showinfo("OK", n.editar(id_nota))
        recarregar()
        win.destroy()

    tk.Button(win, text="Salvar", command=salvar).pack(pady=10)
