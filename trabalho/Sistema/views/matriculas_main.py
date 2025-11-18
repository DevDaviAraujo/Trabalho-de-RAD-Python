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

Matricula = carregar_class("Matricula")
Aluno = carregar_class("Aluno")
Disciplina = carregar_class("Disciplina")


# ---------------- IMPORTANDO AS JANELAS CRUD ---------------- #

def importa_view(caminho, nome):
    path = os.path.join(BASE_DIR, "Sistema", "views", caminho)
    spec = importlib.util.spec_from_file_location(nome, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, nome)

janela_adicionar = importa_view("matricula/adicionar.py", "janela_adicionar")
janela_editar = importa_view("matricula/editar.py", "janela_editar")
janela_excluir = importa_view("matricula/excluir.py", "janela_excluir")


# ---------------- JANELA PRINCIPAL ---------------- #
   
def janela_matriculas(): 
    
    def ajustar_largura():
        for col in cols:
            max_len = max((len(str(tree.set(k, col))) for k in tree.get_children()), default=15)
            tree.column(col, width=max(50, max_len * 9))

    def carregar_dados(cond=""):
        for item in tree.get_children():
            tree.delete(item)

        # 1. CHAMA O MÉTODO COM JOIN PARA OBTER OS NOMES
        # Retorna: (m.id, u.nome, d.nome)
        rows = Matricula.dadosTabela(cond) 
        
        for r in rows:
            tree.insert("", tk.END, values=r)

        ajustar_largura() 

    def buscar(event=None):
        texto = entrada_busca.get().strip()
        
        if texto:
            # 2. CORRIGE A CONDIÇÃO DE BUSCA PARA USAR NOMES (u.nome, d.nome)
            cond = (
                f"u.nome LIKE '%{texto}%' OR "      # Busca pelo Nome do Aluno
                f"d.nome LIKE '%{texto}%'"          # Busca pelo Nome da Disciplina
            )
            carregar_dados(cond)
        else:
            carregar_dados()

    # ... (funções editar e excluir permanecem as mesmas) ...
    # OBS: O ID da matrícula (r[0]) ainda é a única informação usada no CRUD

    def editar():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma matrícula")
            return
        # Pega o ID da Matrícula (coluna 0 do resultado do JOIN)
        id_mat = tree.item(sel, "values")[0] 
        janela_editar(id_mat, carregar_dados)

    def excluir():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma matrícula")
            return
        id_mat = tree.item(sel, "values")[0]
        janela_excluir(id_mat, carregar_dados)

    # ---------------- UI TKINTER ---------------- #

    root = tk.Tk()
    root.title("Gerenciar Matrículas")
    root.geometry("800x450")

    top = tk.Frame(root); top.pack(fill=tk.X, pady=6, padx=10)
    tk.Label(top, text="Buscar:").pack(side=tk.LEFT)
    entrada_busca = tk.Entry(top); entrada_busca.pack(side=tk.LEFT, padx=5)
    entrada_busca.bind('<KeyRelease>', buscar)
    
    tk.Button(top, text="🔎", command=buscar).pack(side=tk.LEFT, padx=3)
    tk.Button(top, text="➕ Adicionar", command=lambda: janela_adicionar(carregar_dados)).pack(side=tk.LEFT, padx=5)
    tk.Button(top, text="✏ Editar", command=editar).pack(side=tk.LEFT, padx=5)
    tk.Button(top, text="🗑 Excluir", command=excluir).pack(side=tk.LEFT, padx=5)

    # 3. CORRIGE AS COLUNAS PARA EXIBIR OS NOMES
    cols = ("ID", "Aluno", "Disciplina")
    tree = ttk.Treeview(root, columns=cols, show="headings")
    
    tree.heading("ID", text="ID")
    tree.heading("Aluno", text="Nome do Aluno")
    tree.heading("Disciplina", text="Disciplina Matriculada")

    tree.column("ID", anchor=tk.CENTER, width=50)
    tree.column("Aluno", anchor=tk.W, width=300)
    tree.column("Disciplina", anchor=tk.W, width=300)

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    carregar_dados()
    root.mainloop()