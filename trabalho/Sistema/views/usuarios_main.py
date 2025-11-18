# usuarios_main.py
import tkinter as tk
from tkinter import ttk, messagebox
import importlib.util
import os
import sys

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

Usuario = carregar_class("Usuario")


# ---------------- IMPORTANDO AS JANELAS CRUD ---------------- #

def importa_view(caminho, nome):
    path = os.path.join(BASE_DIR, "Sistema", "views", caminho)
    spec = importlib.util.spec_from_file_location(nome, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, nome)

janela_adicionar = importa_view("usuario/adicionar.py", "janela_adicionar")
janela_editar = importa_view("usuario/editar.py", "janela_editar")
janela_excluir = importa_view("usuario/excluir.py", "janela_excluir")


# ---------------- JANELA PRINCIPAL ---------------- #
   
def janela_usuarios(): 
    def formatar_cpf(cpf):
        if cpf and cpf.isdigit() and len(cpf) == 11:
            return f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf


    def pegaDados(condicao=""):
        resultados = Usuario.ler(condicao)
        return resultados if isinstance(resultados, list) else []


    def carregar_dados_tabela(condicao=""):
        for item in tree.get_children():
            tree.delete(item)
            
        if condicao:   
            condicao = condicao + f" AND id != {1}"
        else:
            condicao = f"id != {1}"
            
        for row in pegaDados(condicao):
            # row: (id, cpf, nome, email, senha, tipo)
            idu = row[0]
            nome = row[2]
            cpf = formatar_cpf(row[1])
            email = row[3]
            tipo = row[5].capitalize()

            tree.insert(
                "",
                tk.END,
                values=(idu, nome, cpf, email, tipo),
                tags=(row[5],)
            )

        ajustar_largura()


    # --------- AJUSTA LARGURA DAS COLUNAS ---------
    def ajustar_largura():
        for col in columns:
            max_len = max((len(str(tree.set(k, col))) for k in tree.get_children()), default=12)
            tree.column(col, width=max_len * 9)


    # --------- BUSCA INSTANTÂNEA ---------
    def buscar(event=None):
        texto = procurar_entrada.get().strip()

        if not texto:
            carregar_dados_tabela()
            return

        cond = (
            f"nome LIKE '%{texto}%' OR "
            f"cpf LIKE '%{texto}%' OR "
            f"email LIKE '%{texto}%' OR "
            f"tipo LIKE '%{texto}%'"
        )

        carregar_dados_tabela(cond)


    def editar_selecionado():
        sel = tree.focus()
        if not sel:
            messagebox.showinfo("Atenção", "Selecione um usuário")
            return

        vals = tree.item(sel, "values")
        janela_editar(vals[0], carregar_dados_tabela)


    def excluir_selecionado():
        sel = tree.focus()
        if not sel:
            messagebox.showinfo("Atenção", "Selecione um usuário")
            return

        vals = tree.item(sel, "values")
        janela_excluir(vals[0], carregar_dados_tabela)


    def adicionar_usuario():
        janela_adicionar(carregar_dados_tabela)


    # --------- JANELA PRINCIPAL ---------
    root = tk.Tk()
    root.title("Usuários")
    root.geometry("950x480")

    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP, fill=tk.X, padx=6, pady=6)

    tk.Label(top_frame, text="Procurar:").pack(side=tk.LEFT)

    procurar_entrada = tk.Entry(top_frame)
    procurar_entrada.pack(side=tk.LEFT, padx=6)
    procurar_entrada.bind("<KeyRelease>", buscar)  # BUSCA AO DIGITAR

    tk.Button(top_frame, text="🔎", command=buscar).pack(side=tk.LEFT, padx=3)
    tk.Button(top_frame, text="➕ Adicionar", command=adicionar_usuario).pack(side=tk.LEFT, padx=8)
    tk.Button(top_frame, text="✍️ Editar", command=editar_selecionado).pack(side=tk.LEFT, padx=8)
    tk.Button(top_frame, text="🗑️ Excluir", command=excluir_selecionado).pack(side=tk.LEFT, padx=8)

    # --------- TABELA ---------
    table_frame = tk.Frame(root)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    columns = ("Id", "Nome", "CPF", "Email", "Tipo")

    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    # Cabeçalhos mais claros
    tree.heading("Id", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("CPF", text="CPF")
    tree.heading("Email", text="Email")
    tree.heading("Tipo", text="Tipo de Usuário")

    # Cores por tipo
    tree.tag_configure("aluno", foreground="#0055ff")
    tree.tag_configure("professor", foreground="#009933")
    tree.tag_configure("secretaria", foreground="#aa33ff")

    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    vsb.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(fill=tk.BOTH, expand=True)

    carregar_dados_tabela()

    root.mainloop()
