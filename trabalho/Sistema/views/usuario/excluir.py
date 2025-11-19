# excluirUsuario.py
import tkinter as tk
from tkinter import ttk, messagebox
import importlib.util
import os

# ---------------- CARREGANDO AS CLASSES ---------------- #

def carregar_class(nome):
    caminho = os.path.join('Sistema', 'entidades', f'{nome}.py')
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, nome)

Usuario = carregar_class('Usuario')

# ---------------- JANELA ---------------- #

def janela_excluir(id_usuario, recarregar_callback):
    rows = Usuario.ler(f"id = {id_usuario}")
    if not rows:
        messagebox.showerror("Erro", "Usuário não encontrado")
        return
    row = rows[0]  # (id, cpf, nome, email, senha, tipo)

    win = tk.Tk()
    win.title("Excluir Usuário")
    win.geometry("420x180")

    tk.Label(win, text="O seguinte registro será apagado:", font=("Arial", 10, "bold")).pack(pady=8)

    table_frame = tk.Frame(win)
    table_frame.pack(padx=8, pady=4)
    cols = ("Id", "CPF", "Nome", "Email", "Tipo")
    tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=1)
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=80, anchor="center")
    tree.pack()
    tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[5]))
    
    
# ---------------- EXCLUINDO ---------------- #

    def deletar():
        resultado = Usuario.deletar(row[0])
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


    win.mainloop()
