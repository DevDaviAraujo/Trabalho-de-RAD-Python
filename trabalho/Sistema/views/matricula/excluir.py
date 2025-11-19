import tkinter as tk
from tkinter import ttk, messagebox
import os, importlib.util


# ---------------- CARREGAR CLASSES ---------------- #

def carregar_class(nome):
    caminho = os.path.join('Sistema', 'entidades', f'{nome}.py')
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, nome)

Matricula = carregar_class("Matricula")


# ---------------- JANELA EXCLUIR MATRÍCULA ---------------- #

def janela_excluir(id_matricula, recarregar_callback):

    # BUSCA O REGISTRO DA MATRÍCULA
    rows = Matricula.dadosTabela(f"m.id = {id_matricula}")
    if not rows:
        messagebox.showerror("Erro", "Matrícula não encontrada")
        return

    row = rows[0]  
    # row = (id_matricula, nome_aluno, nome_disciplina)

    # JANELA
    win = tk.Toplevel()
    win.title("Excluir Matrícula")
    win.geometry("620x240")
    win.resizable(False, False)

    tk.Label(
        win,
        text="O seguinte registro será apagado:",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    # TREEVIEW
    colunas = ("ID", "Aluno", "Disciplina")

    tree = ttk.Treeview(win, columns=colunas, show="headings", height=1)

    tree.heading("ID", text="ID")
    tree.heading("Aluno", text="Aluno")
    tree.heading("Disciplina", text="Disciplina")

    tree.column("ID", width=60, anchor=tk.CENTER)
    tree.column("Aluno", width=250, anchor=tk.W)
    tree.column("Disciplina", width=250, anchor=tk.W)

    tree.pack(pady=5)

    # INSERE AS INFORMAÇÕES
    tree.insert("", tk.END, values=row)


# ---------------- EXCLUINDO ---------------- #

    def deletar():
        resultado = Matricula.deletar(row[0])
        messagebox.showinfo("Resultado", resultado)
        recarregar_callback()
        win.destroy()

    # BOTÕES
    frame_botoes = tk.Frame(win)
    frame_botoes.pack(pady=10)

    tk.Button(
        frame_botoes,
        text="Cancelar",
        width=12,
        command=win.destroy
    ).pack(side=tk.LEFT, padx=10)

    tk.Button(
        frame_botoes,
        text="🗑️ Deletar",
        width=12,
        bg="#d9534f",
        fg="white",
        command=deletar
    ).pack(side=tk.LEFT, padx=10)

    win.grab_set()    # Torna a janela modal
