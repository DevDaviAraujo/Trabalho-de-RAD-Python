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
Usuario = carregar_class("Usuario")   # ← IMPORTANTE AQUI


# ---------------- JANELA EDITAR ---------------- #

def janela_editar(id_matricula, refresh):
    rows = Matricula.ler(f"id={id_matricula}")
    if not rows:
        messagebox.showerror("Erro", "Matrícula não encontrada")
        return

    # row → (id, aluno_id, disciplina_id)
    row = rows[0]
    aluno_atual = row[1]
    disciplina_atual = row[2]

    win = tk.Toplevel()
    win.title("Editar Matrícula")
    win.geometry("420x240")

    # ==== ALUNOS ==== #
    tk.Label(win, text="Aluno:").grid(row=0, column=0, pady=5, padx=5)

    alunos = Aluno.ler()  # retorna (id_aluno, id_usuario, curso)
    lista_alunos = []
    valor_aluno_atual = ""

    for a in alunos:
        id_aluno = a[0]
        id_usuario = a[1]

        dados_usuario = Usuario.ler(f"id={id_usuario}")
        if dados_usuario:
            nome_usuario = dados_usuario[0][2]  # índice 2 = nome
            item_str = f"{id_aluno} - {nome_usuario}"
        else:
            item_str = f"{id_aluno} - [Usuário não encontrado]"

        lista_alunos.append(item_str)

        # Seleciona automaticamente
        if str(id_aluno) == str(aluno_atual):
            valor_aluno_atual = item_str

    aluno_cb = ttk.Combobox(win, values=lista_alunos, state="readonly", width=35)
    aluno_cb.grid(row=0, column=1)
    aluno_cb.set(valor_aluno_atual)


    # ==== DISCIPLINAS ==== #
    tk.Label(win, text="Disciplina:").grid(row=1, column=0, pady=5, padx=5)

    disciplinas = Disciplina.ler()  # (id_disciplina, nome, id_professor)
    lista_disc = []
    valor_disc_atual = ""

    for d in disciplinas:
        id_disc = d[0]
        nome_disc = d[1]

        item_str = f"{id_disc} - {nome_disc}"
        lista_disc.append(item_str)

        if str(id_disc) == str(disciplina_atual):
            valor_disc_atual = item_str

    disc_cb = ttk.Combobox(win, values=lista_disc, state="readonly", width=35)
    disc_cb.grid(row=1, column=1)
    disc_cb.set(valor_disc_atual)


# ---------------- SALVAR ---------------- #

    def salvar():
        if not aluno_cb.get() or not disc_cb.get():
            messagebox.showwarning("Aviso", "Selecione aluno e disciplina.")
            return

        aluno_id = aluno_cb.get().split(" - ")[0]
        disciplina_id = disc_cb.get().split(" - ")[0]

        m = Matricula(aluno_id, disciplina_id)
        msg = m.editar(id_matricula)

        messagebox.showinfo("OK", msg)
        refresh()
        win.destroy()

    tk.Button(win, text="Salvar Alterações", command=salvar).grid(row=2, column=1, pady=15)
