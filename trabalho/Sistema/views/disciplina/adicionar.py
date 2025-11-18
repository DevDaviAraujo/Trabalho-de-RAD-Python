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

Disciplina = carregar_class("Disciplina")
Usuario = carregar_class("Usuario")
Professor = carregar_class("Professor")


# ---------------- JANELA ---------------- #

def janela_adicionar(reload_callback):
    win = tk.Toplevel()
    win.title("Adicionar Disciplina")
    win.geometry("400x200") # Aumentei um pouco a largura

    tk.Label(win, text="Nome da Disciplina:").grid(row=0, column=0, padx=5, pady=5)
    nome_entry = tk.Entry(win)
    nome_entry.grid(row=0, column=1, padx=5, pady=5)
    
    # --- CORREÇÃO AQUI ---
    tk.Label(win, text="Professor responsável:").grid(row=1, column=0, padx=5, pady=5)
    
    # 1. Busca os dados brutos dos professores
    dados_professores = Professor.ler() 
    lista_para_combobox = []

    # 2. Itera sobre cada professor para achar o nome do usuário correspondente
    for prof in dados_professores:
        # prof é uma tupla: (id_prof, id_usuario, titulacao, area)
        id_prof = prof[0]
        id_usuario = prof[1] 
        
        # 3. Busca os dados do usuário pelo ID
        # Usuario.ler retorna uma lista de tuplas [(id, cpf, nome, ...)]
        dados_usuario = Usuario.ler(f"id = {id_usuario}")
        
        if dados_usuario:
            # Pegamos o primeiro resultado [0] e a coluna do nome [2]
            # (Verifique se o índice 2 é realmente o Nome na sua tabela Usuario)
            nome_usuario = dados_usuario[0][2] 
            lista_para_combobox.append(f"{id_prof} - {nome_usuario}")

    prof_box = ttk.Combobox(win, values=lista_para_combobox, width=30)
    prof_box.grid(row=1, column=1, padx=5, pady=5)
    # ---------------------

    def enviar():
        nome = nome_entry.get().strip()
        if not prof_box.get():
            messagebox.showwarning("Aviso", "Selecione um professor.")
            return

        # Pega só o ID que está antes do traço " - "
        professor_id = prof_box.get().split(" - ")[0]

        if not nome:
            messagebox.showwarning("Aviso", "Preencha o nome da disciplina.")
            return

        # Aqui chamamos a classe Disciplina (certifique-se que ela aceita esses argumentos)
        d = Disciplina(nome, professor_id)
        
        # Se seu método criar() for de instância, use assim:
        msg = d.criar() 
        
        messagebox.showinfo("OK", msg)
        reload_callback()
        win.destroy()

    tk.Button(win, text="Salvar", command=enviar).grid(row=2, column=1, pady=15)