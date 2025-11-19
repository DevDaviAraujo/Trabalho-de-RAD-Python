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

Nota = carregar_class("Nota")


# ---------------- JANELA DE EXCLUSÃO ---------------- #

def janela_excluir(id_nota, recarregar_callback):

    # Busca os dados completos da nota
    rows = Nota.dadosTabela(f"n.id = {id_nota}")
    if not rows:
        messagebox.showerror("Erro", "Nota não encontrada")
        return

    row = rows[0]
    # row = (id, disc_nome, aluno_nome, prof_nome, trabalho, prova, media)

    # Criando janela
    win = tk.Toplevel()
    win.title("Excluir Nota")
    win.geometry("900x260")
    win.resizable(False, False)

    tk.Label(
        win,
        text="A seguinte nota será apagada:",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    # Colunas
    colunas = ("ID", "Disciplina", "Aluno", "Professor", "Trabalho", "Prova", "Média")

    tree = ttk.Treeview(win, columns=colunas, show="headings", height=1)

    for col in colunas:
        tree.heading(col, text=col)

    tree.column("ID", width=50, anchor=tk.CENTER)
    tree.column("Disciplina", width=180, anchor=tk.W)
    tree.column("Aluno", width=160, anchor=tk.W)
    tree.column("Professor", width=160, anchor=tk.W)
    tree.column("Trabalho", width=90, anchor=tk.CENTER)
    tree.column("Prova", width=90, anchor=tk.CENTER)
    tree.column("Média", width=90, anchor=tk.CENTER)

    tree.pack(pady=5)

    # Inserindo os dados
    tree.insert("", tk.END, values=row)

    # Função de exclusão
    def deletar():
        try:
            Nota.deletar(row[0])
            messagebox.showinfo("OK", "Nota excluída!")
            recarregar_callback()
            win.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")

    # Botões
    frame = tk.Frame(win)
    frame.pack(pady=15)

    tk.Button(frame, text="Cancelar", width=12, command=win.destroy)\
        .pack(side=tk.LEFT, padx=10)

    tk.Button(frame, text="🗑️ Deletar", width=12, bg="#d9534f", fg="white",
              command=deletar)\
        .pack(side=tk.LEFT, padx=10)

    win.grab_set()  # Torna modal
