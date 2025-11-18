# editarUsuario.py
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

def validar_cpf_text_input(novo):
    """Só aceita números e no máximo 11 caracteres."""
    return novo.isdigit() and len(novo) <= 11 or novo == ""


def validar_email(email):
    return "@" in email and "." in email


# ---------------- JANELA ---------------- #

def janela_editar(id_usuario, recarregar_callback):

    # buscar dados do usuário
    rows = Usuario.ler("id = %s", (id_usuario,))
    if not rows:
        messagebox.showerror("Erro", "Usuário não encontrado.")
        return

    user = rows[0]  # (id, cpf, nome, email, senha, tipo)
    tipo_original = user[5]

    # buscar dados de aluno
    aluno = None
    professor = None

    if tipo_original == "aluno":
        r = Aluno.ler("id_usuario = %s", (id_usuario,))
        aluno = r[0] if r else None

    elif tipo_original == "professor":
        r = Professor.ler("id_usuario = %s", (id_usuario,))
        professor = r[0] if r else None
   
    win = tk.Toplevel()
    win.title("Editar Usuário")
    win.geometry("400x430")
    win.resizable(False, False)

    # ===== CAMPOS BÁSICOS =====  #
    tk.Label(win, text="CPF:").pack(anchor="w", padx=10, pady=2)
    vcmd_cpf = (win.register(validar_cpf_text_input), "%P")
    cpf_entry = tk.Entry(win, validate="key", validatecommand=vcmd_cpf)
    cpf_entry.insert(0, user[1])
    cpf_entry.pack(fill="x", padx=10)

    tk.Label(win, text="Nome:").pack(anchor="w", padx=10, pady=2)
    nome_entry = tk.Entry(win)
    nome_entry.insert(0, user[2])
    nome_entry.pack(fill="x", padx=10)

    tk.Label(win, text="Email:").pack(anchor="w", padx=10, pady=2)
    email_entry = tk.Entry(win)
    email_entry.insert(0, user[3])
    email_entry.pack(fill="x", padx=10)

    tk.Label(win, text="Senha:").pack(anchor="w", padx=10, pady=2)
    senha_entry = tk.Entry(win, show="*")
    senha_entry.insert(0, user[4])
    senha_entry.pack(fill="x", padx=10)

    tk.Label(win, text="Tipo:").pack(anchor="w", padx=10, pady=2)
    tipo_var = tk.StringVar(value=tipo_original)
    tipo_cb = ttk.Combobox(win, textvariable=tipo_var,
                           values=["secretaria", "professor", "aluno"],
                           state="readonly")
    tipo_cb.pack(fill="x", padx=10)
    
    # ===== CAMPOS ESPECÍFICOS ===== # 
    # Frame aluno
    aluno_frame = tk.Frame(win)
    tk.Label(aluno_frame, text="Curso:").pack(anchor="w", padx=10)
    curso_entry = tk.Entry(aluno_frame)
    if aluno:
        curso_entry.insert(0, aluno[2])
    curso_entry.pack(fill="x", padx=10)

    # Frame professor
    prof_frame = tk.Frame(win)
    tk.Label(prof_frame, text="Titulação:").pack(anchor="w", padx=10)
    titulacao_entry = tk.Entry(prof_frame)
    if professor:
        titulacao_entry.insert(0, professor[2])
    titulacao_entry.pack(fill="x", padx=10)

    tk.Label(prof_frame, text="Área de atuação:").pack(anchor="w", padx=10)
    area_entry = tk.Entry(prof_frame)
    if professor:
        area_entry.insert(0, professor[3])
    area_entry.pack(fill="x", padx=10)

    # esconder/mostrar conforme tipo
    def atualizar_frames(event=None):
        tipo = tipo_var.get()
        aluno_frame.pack_forget()
        prof_frame.pack_forget()

        if tipo == "aluno":
            aluno_frame.pack(fill="x", pady=8)
        elif tipo == "professor":
            prof_frame.pack(fill="x", pady=8)

    tipo_cb.bind("<<ComboboxSelected>>", atualizar_frames)
    
    atualizar_frames()

   
# ---------------- SALVANDO ---------------- #
    
    def salvar():

        cpf = cpf_entry.get().strip()
        nome = nome_entry.get().strip()
        email = email_entry.get().strip()
        senha = senha_entry.get().strip()
        tipo = tipo_var.get()

        if not all([cpf, nome, email, senha]):
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        if not cpf.isdigit() or len(cpf) != 11:
            messagebox.showwarning("Erro", "CPF inválido.")
            return

        if not validar_email(email):
            messagebox.showwarning("Erro", "Email inválido.")
            return

        # Verificar duplicidade
        if Usuario.ler("cpf=%s AND id != %s", (cpf, id_usuario)):
            messagebox.showwarning("Erro", "CPF já cadastrado.")
            return

        if Usuario.ler("email=%s AND id != %s", (email, id_usuario)):
            messagebox.showwarning("Erro", "Email já cadastrado.")
            return

        # Atualiza usuário
        u = Usuario (
            cpf,
            nome.strip().title(),
            email,
            hashlib.blake2b(senha.encode()).hexdigest(),
            tipo
            )
        u.editar(id_usuario)

        # Atualização das tabelas específicas
        if tipo == "aluno":
            c = curso_entry.get().strip()
            if not c:
                messagebox.showwarning("Erro", "Informe o curso!")
                return

            # atualizar ou criar
            if aluno:
                Aluno(id_usuario, c.strip().title()).editar(aluno[0])
            else:
                Aluno(id_usuario, c.strip().title()).criar()

        elif tipo == "professor":
            t = titulacao_entry.get().strip()
            a = area_entry.get().strip()

            if not (t and a):
                messagebox.showwarning("Erro", "Informe todos os dados do professor!")
                return

            if professor:
                Professor(id_usuario, t.strip().title(), a.strip().title()).editar(professor[0])
            else:
                Professor(id_usuario, t.strip().title(), a.strip().title()).criar()

        # se mudou de tipo, apagar registros antigos
        if tipo_original != tipo:

            if tipo_original == "aluno":
                if aluno:
                    Aluno(aluno[0], aluno[2]).deletar()

            if tipo_original == "professor":
                if professor:
                    Professor(professor[0], professor[2], professor[3]).deletar()

        messagebox.showinfo("OK", "Usuário atualizado!")
        recarregar_callback()
        win.destroy()

    # botões
    btn_frame = tk.Frame(win, pady=10)
    btn_frame.pack()
    tk.Button(btn_frame, text="Cancelar", width=12, command=win.destroy).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Salvar", width=12, command=salvar).pack(side="right", padx=10)
    
 