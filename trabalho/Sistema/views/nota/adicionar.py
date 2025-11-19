# adicionarNota.py
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

Aluno = carregar_class("Aluno")
Disciplina = carregar_class("Disciplina")
Professor = carregar_class("Professor")
Matricula = carregar_class("Matricula")
Nota = carregar_class("Nota")


# ---------------- JANELA ADICIONAR NOTA ---------------- #

def janela_adicionar(recarregar):
    win = tk.Toplevel()
    win.title("Adicionar Nota")
    win.geometry("420x420")
    win.resizable(False, False)

    # ---------------- CARREGAMENTO CORRETO DOS ALUNOS ---------------- #

    # Agora retorna: (id_aluno, nome_usuario)
    alunos = Aluno.dadosTabela()

    # Agora exibe só o nome do aluno
    aluno_map = {a[1]: a[0] for a in alunos}

    # ---------------- DISCIPLINAS ---------------- #

    disciplinas = Disciplina.ler()
    disciplina_map = {d[1]: d[0] for d in disciplinas}
    professor_map = {d[0]: d[2] for d in disciplinas}


    # ---------------- INTERFACE ---------------- #

    tk.Label(win, text="Aluno:").pack(pady=5)
    aluno_var = tk.StringVar()
    aluno_cb = ttk.Combobox(win, textvariable=aluno_var, values=list(aluno_map.keys()), state="readonly")
    aluno_cb.pack(fill="x", padx=10)

    tk.Label(win, text="Disciplina:").pack(pady=5)
    disciplina_var = tk.StringVar()
    disciplina_cb = ttk.Combobox(win, textvariable=disciplina_var, state="readonly")
    disciplina_cb.pack(fill="x", padx=10)

    tk.Label(win, text="Nota Trabalho (0–5):").pack(pady=5)
    nota_trabalho_entry = tk.Entry(win)
    nota_trabalho_entry.pack(fill="x", padx=10)

    tk.Label(win, text="Nota Prova (0–5):").pack(pady=5)
    nota_prova_entry = tk.Entry(win)
    nota_prova_entry.pack(fill="x", padx=10)


    # ---------------- CARREGAR DISCIPLINAS BASEADAS NO ALUNO ---------------- #

    def carregar_disciplinas(event=None):
        disciplina_cb.set("")
        disciplina_cb["values"] = []

        aluno_nome = aluno_var.get()
        if not aluno_nome:
            return

        aluno_id = aluno_map[aluno_nome]

        matriculas = Matricula.ler("aluno_id=%s", (aluno_id,))

        if not matriculas:
            messagebox.showwarning("Aviso", "Este aluno não possui matrículas.")
            return

        nomes = []
        for m in matriculas:
            disc_id = m[2]
            disc = Disciplina.ler("id=%s", (disc_id,))[0]
            nomes.append(disc[1])  # Nome da disciplina

        disciplina_cb["values"] = nomes


    aluno_cb.bind("<<ComboboxSelected>>", carregar_disciplinas)


    # ---------------- SALVAR ---------------- #

    def salvar():
        aluno_nome = aluno_var.get()
        disciplina_nome = disciplina_var.get()
        trab_txt = nota_trabalho_entry.get().strip()
        prov_txt = nota_prova_entry.get().strip()

        if not aluno_nome or not disciplina_nome or not trab_txt or not prov_txt:
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            return

        try:
            trab = float(trab_txt)
            prov = float(prov_txt)
            if not (0 <= trab <= 5 and 0 <= prov <= 5):
                raise ValueError
        except:
            messagebox.showwarning("Erro", "Notas devem ser números entre 0 e 5")
            return

        aluno_id = aluno_map[aluno_nome]
        disciplina_id = disciplina_map[disciplina_nome]
        professor_id = professor_map[disciplina_id]

        matricula = Matricula.ler(
            "aluno_id=%s AND disciplina_id=%s",
            (aluno_id, disciplina_id)
        )

        if not matricula:
            messagebox.showerror("Erro", "Aluno não está matriculado nesta disciplina.")
            return

        matricula_id = matricula[0][0]

        nova = Nota(disciplina_id, aluno_id, professor_id, trab, prov, matricula_id)

        messagebox.showinfo("OK", nova.criar())
        recarregar()
        win.destroy()


    tk.Button(win, text="Salvar", command=salvar).pack(pady=20)

    win.grab_set()
