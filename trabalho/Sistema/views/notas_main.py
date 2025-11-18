# notas_main.py
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
Aluno = carregar_class("Aluno")
Disciplina = carregar_class("Disciplina")
Matricula = carregar_class("Matricula")
Professor = carregar_class("Professor")


# ---------------- IMPORTANDO AS JANELAS CRUD ---------------- #

def importa_view(caminho, nome):
    path = os.path.join(BASE_DIR, "Sistema", "views", caminho)
    spec = importlib.util.spec_from_file_location(nome, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, nome)

janela_adicionar = importa_view("nota/adicionar.py", "janela_adicionar")
janela_editar = importa_view("nota/editar.py", "janela_editar")
janela_excluir = importa_view("nota/excluir.py", "janela_excluir")


 # ---------------- JANELA PRINCIPAL ---------------- #
    
def janela_notas(): 
    
    def ajustar_largura():
        for col in columns:
            max_len = max((len(str(tree.set(k, col))) for k in tree.get_children()), default=10)
            # Larguras ajustadas para as notas e nomes
            if col in ("Trabalho", "Prova", "Média"):
                 tree.column(col, width=80, anchor=tk.CENTER)
            elif col == "ID":
                 tree.column(col, width=50, anchor=tk.CENTER)
            else:
                 tree.column(col, width=max(150, max_len * 9), anchor=tk.W)

    def carregar_tabela(cond=""):
        for i in tree.get_children():
            tree.delete(i)

        # 1. CHAMA O MÉTODO COM JOIN PARA OBTER OS NOMES E A MÉDIA
        rows = Nota.dadosTabela(cond)
        
        for row in rows:
            # row: (ID, Nome Disciplina, Nome Aluno, Nome Professor, Nota Trabalho, Nota Prova, Média)
            # Formata a média para 2 casas decimais
            dados_formatados = list(row)
            media = dados_formatados[6]
            dados_formatados[6] = f"{media:.2f}" 

            tree.insert("", tk.END, values=dados_formatados)
        
        ajustar_largura()


    def buscar(event=None):
        entrada = entrada_busca.get().strip()
        if entrada:
            # 2. CONDIÇÃO DE BUSCA AJUSTADA PARA USAR OS ALIASES DO JOIN
            cond = (
                f"u_aluno.nome LIKE '%{entrada}%' OR "  # Busca por Nome do Aluno
                f"d.nome LIKE '%{entrada}%' OR "        # Busca por Nome da Disciplina
                f"u_prof.nome LIKE '%{entrada}%'"       # Busca por Nome do Professor
            )
            carregar_tabela(cond)
        else:
            carregar_tabela()


    def adicionar():
        janela_adicionar(carregar_tabela)

    def editar():
        sel = tree.focus()
        if not sel:
            messagebox.showinfo("Atenção", "Selecione uma nota")
            return
        # Pega o ID da Nota (coluna 0, que é o ID da tabela 'notas')
        nota_id = tree.item(sel, "values")[0] 
        janela_editar(nota_id, carregar_tabela)

    def excluir():
        sel = tree.focus()
        if not sel:
            messagebox.showinfo("Atenção", "Selecione uma nota")
            return
        nota_id = tree.item(sel, "values")[0]
        janela_excluir(nota_id, carregar_tabela)

    # ---------------- UI TKINTER ---------------- #
    root = tk.Tk()
    root.title("Gerenciar Lançamento de Notas")
    root.geometry("1000x500")

    top = tk.Frame(root)
    top.pack(fill="x", pady=10, padx=10)

    # Barra de busca
    tk.Label(top, text="Buscar:").pack(side="left")
    entrada_busca = tk.Entry(top)
    entrada_busca.pack(side="left", padx=5)
    entrada_busca.bind('<KeyRelease>', buscar)

    tk.Button(top, text="🔎", command=buscar).pack(side="left", padx=3)
    tk.Button(top, text="➕ Adicionar Nota", command=adicionar).pack(side="left", padx=(15, 5))
    tk.Button(top, text="✏️ Editar", command=editar).pack(side="left", padx=5)
    tk.Button(top, text="🗑️ Excluir", command=excluir).pack(side="left", padx=5)

    # 3. COLUNAS ATUALIZADAS PARA EXIBIR NOMES E MÉDIA
    columns = ("ID", "Disciplina", "Aluno", "Professor", "Trabalho", "Prova", "Média")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.pack(expand=True, fill="both", padx=10, pady=5)

    tree.heading("ID", text="ID")
    tree.heading("Disciplina", text="Disciplina")
    tree.heading("Aluno", text="Aluno")
    tree.heading("Professor", text="Professor")
    tree.heading("Trabalho", text="Trab. (5.0)")
    tree.heading("Prova", text="Prova (5.0)")
    tree.heading("Média", text="MÉDIA")

    carregar_tabela()
    root.mainloop()