import tkinter as tk
from tkinter import ttk, messagebox
import importlib.util, os, sys

# Ajustar sys.path para acessar o diretório raiz
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

Disciplina = carregar_class("Disciplina")
Professor = carregar_class("Professor")


# ---------------- IMPORTANDO AS JANELAS CRUD ---------------- #

def importa_view(caminho, nome):
    path = os.path.join(BASE_DIR, "Sistema", "views", caminho)
    spec = importlib.util.spec_from_file_location(nome, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, nome)

janela_adicionar = importa_view("disciplina/adicionar.py", "janela_adicionar")
janela_editar = importa_view("disciplina/editar.py", "janela_editar")
janela_excluir = importa_view("disciplina/excluir.py", "janela_excluir")


# ---------------- JANELA PRINCIPAL ---------------- #
    
def janela_disciplinas(): 
    
    # Função auxiliar para ajustar a largura das colunas
    def ajustar_largura():
        for col in cols:
            max_len = max((len(str(tree.set(k, col))) for k in tree.get_children()), default=15)
            # Define uma largura mínima e permite expansão com base no conteúdo
            tree.column(col, width=max(60, max_len * 9))
            
    def carregar_dados(cond=""):
        for item in tree.get_children():
            tree.delete(item)

        # 1. CHAMA O MÉTODO COM JOIN PARA OBTER O NOME DO PROFESSOR
        # O método dadosTabela retorna: (d.id, d.nome, u.nome AS nome_professor)
        rows = Disciplina.dadosTabela(cond) 
        
        for r in rows:
            # r: (ID da Disciplina, Nome da Disciplina, Nome do Professor)
            tree.insert("", tk.END, values=r)

        ajustar_largura() # Ajusta a largura após carregar

    def buscar(event=None):
        texto = entrada_busca.get().strip()
        
        if texto:
            # 2. CORRIGE A CONDIÇÃO DE BUSCA PARA USAR OS ALIASES DO JOIN (d.nome, u.nome)
            cond = (
                f"d.nome LIKE '%{texto}%' OR "  # Busca pelo nome da Disciplina
                f"u.nome LIKE '%{texto}%'"      # Busca pelo nome do Professor
            )
            carregar_dados(cond)
        else:
            carregar_dados()

    def editar():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um item")
            return
            
        # Pega o ID da disciplina (coluna 0 da tupla na treeview)
        id_disc = tree.item(sel, "values")[0] 
        janela_editar(id_disc, carregar_dados)

    def excluir():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um item")
            return
        id_disc = tree.item(sel, "values")[0]
        janela_excluir(id_disc, carregar_dados)

    root = tk.Tk()
    root.title("Gerenciar Disciplinas")
    root.geometry("800x400") # Aumentado para caber os nomes completos
    root.bind('<KeyRelease>', buscar) # Opcional: Busca ao digitar no root

    top = tk.Frame(root); top.pack(fill=tk.X, pady=6, padx=10)
    tk.Label(top, text="Buscar:").pack(side=tk.LEFT)
    
    entrada_busca = tk.Entry(top)
    entrada_busca.pack(side=tk.LEFT, padx=5)
    entrada_busca.bind('<KeyRelease>', buscar) # Busca ao digitar na caixa
    
    tk.Button(top, text="🔎", command=buscar).pack(side=tk.LEFT, padx=3)
    tk.Button(top, text="➕ Adicionar", command=lambda: janela_adicionar(carregar_dados)).pack(side=tk.LEFT, padx=5)
    tk.Button(top, text="✏ Editar", command=editar).pack(side=tk.LEFT, padx=5)
    tk.Button(top, text="🗑 Excluir", command=excluir).pack(side=tk.LEFT, padx=5)

    # 3. CORRIGE AS COLUNAS PARA REFLETIR O NOME DO PROFESSOR (em vez do ID)
    cols = ("ID", "Nome da Disciplina", "Professor Responsável")
    tree = ttk.Treeview(root, columns=cols, show="headings")
    
    tree.heading("ID", text="ID")
    tree.heading("Nome da Disciplina", text="Disciplina")
    tree.heading("Professor Responsável", text="Professor")

    tree.column("ID", anchor=tk.CENTER, width=50)
    tree.column("Nome da Disciplina", anchor=tk.W, width=300)
    tree.column("Professor Responsável", anchor=tk.W, width=250)

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    carregar_dados()
    root.mainloop()