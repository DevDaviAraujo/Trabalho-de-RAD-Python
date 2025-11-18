import tkinter as tk
from tkinter import ttk, messagebox
import importlib.util, os


# ---------------- CARREGANDO AS CLASSES ---------------- #

def carregar_class(nome):
    caminho = os.path.join('Sistema', 'entidades', f'{nome}.py')
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, nome)

Matricula = carregar_class("Matricula")
Aluno = carregar_class("Aluno")
Disciplina = carregar_class("Disciplina")


# ---------------- JANELA ---------------- #

def janela_editar(id_matricula, refresh):
    rows = Matricula.ler(f"id={id_matricula}")
    if not rows:
        messagebox.showerror("Erro", "Matrícula não encontrada")
        return

    row = rows[0]

    win = tk.Toplevel()
    win.title("Editar Matrícula")
    win.geometry("350x220")

    tk.Label(win, text="Aluno:").grid(row=0, column=0, pady=5, padx=5)
    alunos = Aluno.ler()
    aluno_cb = ttk.Combobox(win, values=[f"{a[0]} - Usuário {a[1]}" for a in alunos], state="readonly")
    aluno_cb.grid(row=0, column=1)
    aluno_cb.set(row[1])

    tk.Label(win, text="Disciplina:").grid(row=1, column=0, pady=5, padx=5)
    disciplinas = Disciplina.ler()
    disc_cb = ttk.Combobox(win, values=[f"{d[0]} - {d[1]}" for d in disciplinas], state="readonly")
    disc_cb.grid(row=1, column=1)
    disc_cb.set(row[2])


# ---------------- SALVANDO ---------------- #

    def salvar():
        aluno_id = aluno_cb.get().split(" - ")[0]
        disciplina_id = disc_cb.get().split(" - ")[0]

        m = Matricula(aluno_id, disciplina_id)
        msg = m.editar(id_matricula)

        messagebox.showinfo("OK", msg)
        refresh()
        win.destroy()

    tk.Button(win, text="Salvar", command=salvar).grid(row=2, column=1, pady=15)
