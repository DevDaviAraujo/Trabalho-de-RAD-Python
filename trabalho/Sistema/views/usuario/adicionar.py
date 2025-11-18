import tkinter as tk
from tkinter import ttk, messagebox
import importlib.util
import os
import hashlib


# ---------------- CARREGANDO AS CLASSES ---------------- #

def carregar_class(nome):
    caminho = os.path.join('Sistema', 'entidades', f'{nome}.py')
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, nome)

Usuario = carregar_class("Usuario")
Aluno = carregar_class("Aluno")
Professor = carregar_class("Professor")


# ---------------- VALIDADORES (INPUT) ---------------- #

def validar_input_cpf(valor):
    """Permite somente números e no máximo 11 dígitos."""
    if valor.isdigit() and len(valor) <= 11:
        return True
    if valor == "":  # permite apagar tudo
        return True
    return False


def validar_email(email):
    """Validação simples."""
    return "@" in email and "." in email


# ---------------- JANELA ---------------- #

def janela_adicionar(recarregar_callback):
    def atualizar_frames(*args):
        tipo = tipo_var.get()
        aluno_frame.pack_forget()
        prof_frame.pack_forget()

        if tipo == "aluno":
            aluno_frame.pack(fill="x", padx=6, pady=6)
        elif tipo == "professor":
            prof_frame.pack(fill="x", padx=6, pady=6)

    win = tk.Toplevel()
    win.title("Adicionar Usuário")
    win.geometry("400x480")

    # VALIDATOR DE CPF (input)
    validar_cpf_cmd = win.register(validar_input_cpf)

    # CPF
    tk.Label(win, text="CPF (somente números, máx 11):").pack(anchor="w", padx=6)
    cpf_entry = tk.Entry(win, validate="key",
                         validatecommand=(validar_cpf_cmd, "%P"))
    cpf_entry.pack(fill="x", padx=6, pady=3)

    # Nome
    tk.Label(win, text="Nome:").pack(anchor="w", padx=6)
    nome_entry = tk.Entry(win)
    nome_entry.pack(fill="x", padx=6, pady=3)

    # Email
    tk.Label(win, text="Email:").pack(anchor="w", padx=6)
    email_entry = tk.Entry(win)
    email_entry.pack(fill="x", padx=6, pady=3)

    # Senha
    tk.Label(win, text="Senha:").pack(anchor="w", padx=6)
    senha_entry = tk.Entry(win, show="*")
    senha_entry.pack(fill="x", padx=6, pady=3)

    # Tipo
    tk.Label(win, text="Tipo:").pack(anchor="w", padx=6)
    tipo_var = tk.StringVar()
    tipo_cb = ttk.Combobox(win, textvariable=tipo_var,
                           values=["aluno", "professor", "secretaria"],
                           state="readonly")
    tipo_cb.pack(fill="x", padx=6, pady=3)
    tipo_cb.bind("<<ComboboxSelected>>", atualizar_frames)
    tipo_var.set("aluno")  # padrão

    # Frame aluno
    aluno_frame = tk.Frame(win)
    tk.Label(aluno_frame, text="Curso:").pack(anchor="w", padx=6)
    curso_entry = tk.Entry(aluno_frame)
    curso_entry.pack(fill="x", padx=6, pady=3)

    # Frame professor
    prof_frame = tk.Frame(win)
    tk.Label(prof_frame, text="Titulação:").pack(anchor="w", padx=6)
    titulacao_entry = tk.Entry(prof_frame)
    titulacao_entry.pack(fill="x", padx=6, pady=3)

    tk.Label(prof_frame, text="Área de atuação:").pack(anchor="w", padx=6)
    area_entry = tk.Entry(prof_frame)
    area_entry.pack(fill="x", padx=6, pady=3)

    atualizar_frames()
    
# ---------------- SALVANDO ---------------- #    
    
    def salvar():
        cpf = cpf_entry.get().strip()
        nome = nome_entry.get().strip()
        email = email_entry.get().strip()
        senha = senha_entry.get().strip()
        tipo = tipo_var.get()

        # Validações 
        if len(cpf) != 11:
            messagebox.showwarning("Erro", "CPF deve conter 11 dígitos!")
            return
        
        if not validar_email(email):
            messagebox.showwarning("Erro", "E-mail inválido!")
            return

        if Usuario.ler("cpf=%s", (cpf,)):
            messagebox.showwarning("Erro", "CPF já cadastrado!")
            return

        if Usuario.ler("email=%s", (email,)):
            messagebox.showwarning("Erro", "Email já cadastrado!")
            return

        # Criar usuário
        usuario = Usuario (
            cpf,
            nome.strip().title(),
            email,
            hashlib.blake2b(senha.encode()).hexdigest(),
            tipo
            )
        
        id_usuario = usuario.criar()

        if isinstance(id_usuario, str):
            messagebox.showerror("Erro ao cadastrar usuário", id_usuario)
            return

        # Criar aluno ou professor
        if tipo == "aluno":
            curso = curso_entry.get().strip()
            if not curso:
                messagebox.showwarning("Erro", "Informe o curso do aluno!")
                return

            aluno = Aluno (
                id_usuario,
                curso.strip().title()
                )
            aluno.criar()

        elif tipo == "professor":
            titulacao = titulacao_entry.get().strip()
            area = area_entry.get().strip()

            if not titulacao or not area:
                messagebox.showwarning("Erro", "Preencha os dados do professor!")
                return

            prof = Professor (
                id_usuario,
                titulacao.strip().title(),
                area.strip().title()
                )
            prof.criar()

        messagebox.showinfo("Sucesso", "Cadastro concluído!")
        recarregar_callback()
        win.destroy()

    # Botões
    btn_frame = tk.Frame(win)
    btn_frame.pack(fill="x", pady=15)
    tk.Button(btn_frame, text="Cancelar", command=win.destroy).pack(side="left", padx=20)
    tk.Button(btn_frame, text="Salvar", command=salvar).pack(side="right", padx=20)
    
    


