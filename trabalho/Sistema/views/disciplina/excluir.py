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

Disciplina = carregar_class("Disciplina")


# ---------------- JANELA EXCLUIR ---------------- #

def janela_excluir(id_disciplina, recarregar_callback):

    rows = Disciplina.dadosTabela(f"d.id = {id_disciplina}")  # <-- CORRIGIDO
    if not rows:
        messagebox.showerror("Erro", "Disciplina não encontrada")
        return

    row = rows[0]  # (id, nome_disciplina, nome_professor)

    win = tk.Toplevel()
    win.title("Excluir Disciplina")
    win.geometry("600x220")
    win.resizable(False, False)

    tk.Label(win,
             text="O seguinte registro será apagado:",
             font=("Arial", 12, "bold")
             ).pack(pady=10)

    # --- TABLE VIEW --- #
    cols = ("ID", "Disciplina", "Professor")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=1)

    tree.heading("ID", text="ID")
    tree.heading("Disciplina", text="Nome da Disciplina")
    tree.heading("Professor", text="Professor Responsável")

    tree.column("ID", anchor=tk.CENTER, width=60)
    tree.column("Disciplina", anchor=tk.W, width=250)
    tree.column("Professor", anchor=tk.W, width=250)

    tree.pack(pady=5)

    # INSERE OS DADOS
    tree.insert("", "end", values=(row[0], row[1], row[2]))

# ---------------- EXCLUINDO ---------------- #

    def deletar():
        resultado = Disciplina.deletar(row[0])
        messagebox.showinfo("Resultado", resultado)
        recarregar_callback()
        win.destroy()

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Cancelar",
              width=12, command=win.destroy).pack(side=tk.LEFT, padx=10)

    tk.Button(btn_frame, text="🗑️ Deletar", width=12,
              bg="#d9534f", fg="white",
              command=deletar).pack(side=tk.LEFT, padx=10)

    win.grab_set() 
