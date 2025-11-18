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


# ---------------- JANELA ---------------- #

def janela_adicionar(recarregar):
    win = tk.Toplevel()
    win.title("Adicionar Nota")
    win.geometry("400x380")

    def carregar_disciplinas(event=None):
        aluno = aluno_var.get()
        if not aluno:
            return

        aluno_id = aluno_map[aluno]
        matriculas = Matricula.ler("aluno_id=%s", (aluno_id,))

        disciplina_var.set("")
        disciplina_cb["values"] = []

        if not matriculas:
            return

        lista = []
        for m in matriculas:
            disc = Disciplina.ler("id=%s", (m[2],))[0]
            lista.append(disc[1])  # nome

        disciplina_cb["values"] = lista

    # Carregar alunos
    alunos = Aluno.ler("")
    aluno_map = {a[0]: a[0] for a in alunos}
    aluno_map = {f"{a[0]} - {a[1]}": a[0] for a in alunos}

    # Carregar disciplinas e professores
    disciplinas = Disciplina.ler("")
    disciplina_map = {d[1]: d[0] for d in disciplinas}
    professor_map = {d[0]: d[2] for d in disciplinas}  # disciplina_id → professor_id

    tk.Label(win, text="Aluno:").pack()
    aluno_var = tk.StringVar()
    aluno_cb = ttk.Combobox(win, textvariable=aluno_var, values=list(aluno_map.keys()))
    aluno_cb.pack(fill="x")
    aluno_cb.bind("<<ComboboxSelected>>", carregar_disciplinas)

    tk.Label(win, text="Disciplina:").pack()
    disciplina_var = tk.StringVar()
    disciplina_cb = ttk.Combobox(win, textvariable=disciplina_var, state="readonly")
    disciplina_cb.pack(fill="x")

    tk.Label(win, text="Nota Trabalho (0–5):").pack()
    nota_trabalho_entry = tk.Entry(win)
    nota_trabalho_entry.pack(fill="x")

    tk.Label(win, text="Nota Prova (0–5):").pack()
    nota_prova_entry = tk.Entry(win)
    nota_prova_entry.pack(fill="x")
    
    
# ---------------- SALVANDO ---------------- #

    def salvar():
        aluno_nome = aluno_var.get()
        disciplina_nome = disciplina_var.get()
        nota_trab = nota_trabalho_entry.get().strip()
        nota_prov = nota_prova_entry.get().strip()

        if not aluno_nome or not disciplina_nome or not nota_trab or not nota_prov:
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            return

        try:
            trab = float(nota_trab)
            prov = float(nota_prov)
            if not (0 <= trab <= 5 and 0 <= prov <= 5):
                raise ValueError
        except:
            messagebox.showwarning("Erro", "Notas devem ser números entre 0 e 5")
            return

        aluno_id = aluno_map[aluno_nome]
        disciplina_id = disciplina_map[disciplina_nome]
        professor_id = professor_map[disciplina_id]

        m = Matricula.ler(
            "aluno_id=%s AND disciplina_id=%s",
            (aluno_id, disciplina_id)
        )[0][0]

        nova = Nota(disciplina_id, aluno_id, professor_id, trab, prov, m)
        messagebox.showinfo("OK", nova.criar())
        recarregar()
        win.destroy()

    tk.Button(win, text="Salvar", command=salvar).pack(pady=10)
