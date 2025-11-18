import tkinter as tk
from tkinter import ttk, messagebox
import os, importlib.util


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


# ---------------- JANELA EDITAR ---------------- #

def janela_editar(id_disciplina, reload_callback):
    # 1. Busca os dados da DISCIPLINA atual
    rows = Disciplina.ler(f"id={id_disciplina}")
    if not rows:
        messagebox.showerror("Erro", "Disciplina não encontrada")
        return
    
    # rows[0] retorna a tupla do banco, ex: (1, 'Matemática', 5) -> (id, nome, id_professor)
    disciplina_atual = rows[0] 
    nome_atual_disciplina = disciplina_atual[1] # Índice 1 é o Nome
    id_professor_atual = disciplina_atual[2]    # Índice 2 é o ID do Professor
    
    # 2. Busca dados para preencher o COMBOBOX (Lista de Professores)
    dados_professores = Professor.ler() 
    lista_combobox = []
    valor_para_selecionar = "" # Variável para guardar o texto do professor atual

    # Loop para criar strings "ID - Nome"
    for prof in dados_professores:
        # prof estrutura provável: (id_prof, id_usuario, titulacao, area)
        id_prof = prof[0]
        id_usuario = prof[1] 
        
        # Busca o nome na tabela Usuários
        dados_usuario = Usuario.ler(f"id = {id_usuario}")
        
        if dados_usuario:
            # dados_usuario[0] é a tupla do usuário. Índice [2] assumimos ser o Nome.
            nome_usuario = dados_usuario[0][2] 
            
            # Cria a string formatada
            item_str = f"{id_prof} - {nome_usuario}"
            lista_combobox.append(item_str)
            
            # LÓGICA CRUCIAL: Se o ID deste professor for igual ao salvo na disciplina,
            # guardamos essa string para deixar selecionado automaticamente.
            if str(id_prof) == str(id_professor_atual):
                valor_para_selecionar = item_str

    # 3. Montagem da Janela
    win = tk.Toplevel()
    win.title("Editar Disciplina")
    win.geometry("350x200")

    tk.Label(win, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
    nome_entry = tk.Entry(win)
    nome_entry.grid(row=0, column=1, padx=5, pady=5)
    
    # Preenche o campo nome com o valor atual
    nome_entry.insert(0, nome_atual_disciplina)

    tk.Label(win, text="Professor:").grid(row=1, column=0, padx=5, pady=5)
    
    # Cria o combobox com a lista que montamos acima
    prof_box = ttk.Combobox(win, values=lista_combobox, width=30)
    prof_box.grid(row=1, column=1, padx=5, pady=5)
    
    # Seleciona o professor atual automaticamente
    if valor_para_selecionar:
        prof_box.set(valor_para_selecionar)


# ---------------- SALVANDO ---------------- #
    
    def salvar():
        nome = nome_entry.get().strip()
        
        # Validações básicas
        if not nome:
            messagebox.showwarning("Aviso", "O nome não pode ser vazio")
            return
            
        if not prof_box.get():
            messagebox.showwarning("Aviso", "Selecione um professor")
            return

        # Pega o ID antes do traço " - "
        professor_id_novo = prof_box.get().split(" - ")[0]

        # Cria instância (assumindo que o construtor aceita nome, id_prof)
        d = Disciplina(nome, professor_id_novo)
        
        # Chama o método de editar passando o ID da disciplina que estamos editando
        msg = d.editar(id_disciplina)

        messagebox.showinfo("Sucesso", msg)
        reload_callback() # Atualiza a tabela na janela principal
        win.destroy() # Fecha a janelinha

    tk.Button(win, text="Salvar Alterações", command=salvar).grid(row=2, column=1, pady=15)