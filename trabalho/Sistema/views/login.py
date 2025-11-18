import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import importlib.util
import hashlib
from PIL import Image, ImageTk, ImageDraw
import math

# --- Base do projeto ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ---------------- CONFIGURAÇÕES VISUAIS ---------------- #

# Convertendo os RGBs solicitados para Hexadecimal
# RGB(117,0,91) -> #75005b
# RGB(189,24,32) -> #bd1820
COR_INICIAL = "#75005b"
COR_FINAL = "#bd1820"
ANGULO = 45
CAMINHO_IMAGEM_LOGO = r"Sistema\imagem\newton-paiva.webp"


# ---------------- CARREGANDO AS CLASSES ---------------- #

def carregar_class(nome):
    caminho = os.path.join('Sistema', 'entidades', f'{nome}.py')
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, nome)

Usuario = carregar_class("Usuario")


# ---------------- IMPORTANDO AS JANELAS CRUD ---------------- #

def importa_view(caminho_relativo, nome_funcao):
    try:
        path = os.path.join(BASE_DIR, "Sistema", "views", caminho_relativo)
        if not os.path.exists(path):
             path = os.path.join("Sistema", "views", caminho_relativo)
             
        spec = importlib.util.spec_from_file_location(nome_funcao, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return getattr(mod, nome_funcao)
    except Exception as e:
        print(f"Aviso: Não foi possível carregar a view {nome_funcao}. ({e})")
        return lambda: messagebox.showinfo("Info", "Janela não encontrada.")

janela_disciplinas = importa_view("disciplinas_main.py", "janela_disciplinas")
janela_notas = importa_view("notas_main.py", "janela_notas")
janela_usuarios = importa_view("usuarios_main.py", "janela_usuarios")
janela_matriculas = importa_view("matriculas_main.py", "janela_matriculas")


# ---------------- FUNÇÕES DE DEGRADÊ ---------------- #

def hex_para_rgb(hex_color):
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def interpolar_cor(cor1, cor2, fator):
    r1, g1, b1 = cor1
    r2, g2, b2 = cor2
    r = int(r1 + (r2 - r1) * fator)
    g = int(g1 + (g2 - g1) * fator)
    b = int(b1 + (b2 - b1) * fator)
    return (r, g, b)

def criar_imagem_gradiente(largura, altura, cor_inicial, cor_final, angulo_deg):
    rgb_inicial = hex_para_rgb(cor_inicial)
    rgb_final = hex_para_rgb(cor_final)
    
    img = Image.new("RGB", (largura, altura))
    pixels = img.load()
    
    angulo_rad = math.radians(angulo_deg)
    cos_a = math.cos(angulo_rad)
    sin_a = math.sin(angulo_rad)
    
    # Cálculos para a projeção do gradiente
    pontos_canto = [(0, 0), (largura, 0), (0, altura), (largura, altura)]
    projecoes = [x * cos_a + y * sin_a for x, y in pontos_canto]
    p_min = min(projecoes)
    p_max = max(projecoes)
    dist_total = p_max - p_min if p_max != p_min else 1
    
    for y in range(altura):
        for x in range(largura):
            projecao = x * cos_a + y * sin_a
            fator = (projecao - p_min) / dist_total
            fator = max(0.0, min(1.0, fator))
            pixels[x, y] = interpolar_cor(rgb_inicial, rgb_final, fator)
            
    return img

def aplicar_fundo_degrade(janela, largura, altura):
    """Aplica o degradê como background de uma janela."""
    imagem_pillow = criar_imagem_gradiente(largura, altura, COR_INICIAL, COR_FINAL, ANGULO)
    imagem_tkinter = ImageTk.PhotoImage(imagem_pillow)
    
    bg_label = tk.Label(janela, image=imagem_tkinter)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Guarda referência para o Garbage Collector não apagar
    janela.imagem_fundo = imagem_tkinter
    return bg_label


# ---------------- LOGANDO USUÁRIO ---------------- #

def tentar_login():
    cpf = cpf_entry.get().strip()
    senha = senha_entry.get().strip()
    senha_hash = hashlib.blake2b(senha.encode()).hexdigest()

    if not cpf or not senha:
        messagebox.showwarning("Atenção", "Preencha todos os campos")
        return

    # Buscar usuário no banco
    rows = Usuario.ler("cpf=%s AND senha=%s", (cpf, senha_hash))

    if not rows:
        messagebox.showerror("Erro", "CPF ou senha incorretos")
        return

    usuario = rows[0]
    # Ajuste o índice conforme sua tabela real (no exemplo usei 5 para tipo)
    # Geralmente: id, nome, cpf, email, senha, tipo -> tipo é index 5
    tipo = usuario[5] if len(usuario) > 5 else "aluno" 

    root.destroy()
    abrir_menu_inicial(tipo)


# ---------------- JANELA MENU DE OPÇÕES ---------------- #

def abrir_menu_inicial(tipo_usuario):
    menu = tk.Tk()
    menu.title("Painel de Controle")
    
    LARGURA = 500
    ALTURA = 400
    x_pos = (menu.winfo_screenwidth() - LARGURA) // 2
    y_pos = (menu.winfo_screenheight() - ALTURA) // 2
    menu.geometry(f"{LARGURA}x{ALTURA}+{x_pos}+{y_pos}")
    
    # 1. Aplica o fundo degradê
    aplicar_fundo_degrade(menu, LARGURA, ALTURA)
    
    # 2. Container Branco (Card)
    card_frame = tk.Frame(menu, bg="white", padx=20, pady=20, bd=2, relief="raised")
    card_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(card_frame, text=f"Bem-vindo, {tipo_usuario.capitalize()}!", 
             font=("Arial", 14, "bold"), bg="white", fg="#333").pack(pady=(0, 15))

    # Estilo dos botões
    btn_config = {"width": 25, "bg": "#f0f0f0", "relief": "groove", "pady": 5}

    if tipo_usuario == "secretaria":
        tk.Button(card_frame, text="Gerenciar Usuários", command=lambda: janela_usuarios(), **btn_config).pack(pady=5)
        tk.Button(card_frame, text="Gerenciar Disciplinas", command=lambda: janela_disciplinas(), **btn_config).pack(pady=5)
        tk.Button(card_frame, text="Gerenciar Matrículas", command=lambda: janela_matriculas(), **btn_config).pack(pady=5)
        tk.Button(card_frame, text="Gerenciar Notas", command=lambda: janela_notas(), **btn_config).pack(pady=5)
    
    elif tipo_usuario == "professor":
        tk.Button(card_frame, text="Notas das Matrículas", command=lambda: janela_matriculas(), **btn_config).pack(pady=10)

    elif tipo_usuario == "aluno":
        tk.Button(card_frame, text="Minhas Notas", command=lambda: janela_notas(), **btn_config).pack(pady=10)

    tk.Button(card_frame, text="Sair", command=menu.destroy, bg="#ffcccc", width=25).pack(pady=15)

    menu.mainloop()


# ---------------- JANELA DO LOGIN ---------------- #

def validar_input_cpf(valor):
    if valor.isdigit() and len(valor) <= 11:
        return True
    if valor == "":
        return True
    return False

# Configuração da Janela Principal
root = tk.Tk()
root.title("Sistema Acadêmico - Login")

# Dimensões maiores para caber a imagem e ficar bonito
LARGURA_LOGIN = 400
ALTURA_LOGIN = 500
x_pos = (root.winfo_screenwidth() - LARGURA_LOGIN) // 2
y_pos = (root.winfo_screenheight() - ALTURA_LOGIN) // 2
root.geometry(f"{LARGURA_LOGIN}x{ALTURA_LOGIN}+{x_pos}+{y_pos}")
root.resizable(False, False)

# 1. Aplica Fundo Degradê
aplicar_fundo_degrade(root, LARGURA_LOGIN, ALTURA_LOGIN)

# 2. Frame Central (Card Branco)
frame_card = tk.Frame(root, bg="white", bd=2, relief="raised")
frame_card.place(relx=0.5, rely=0.5, anchor="center", width=320, height=420)

# 3. Carregar e Exibir Imagem (Logo)
try:
    if os.path.exists(CAMINHO_IMAGEM_LOGO):
        img_original = Image.open(CAMINHO_IMAGEM_LOGO)
        # Redimensionar mantendo proporção (máx 200px de largura)
        base_width = 200
        w_percent = (base_width / float(img_original.size[0]))
        h_size = int((float(img_original.size[1]) * float(w_percent)))
        img_resized = img_original.resize((base_width, h_size), Image.Resampling.LANCZOS)
        
        logo_tk = ImageTk.PhotoImage(img_resized)
        lbl_img = tk.Label(frame_card, image=logo_tk, bg="white")
        lbl_img.image = logo_tk # Referência
        lbl_img.pack(pady=(20, 10))
    else:
        tk.Label(frame_card, text="Imagem não encontrada", bg="white", fg="red").pack(pady=10)
except Exception as e:
    tk.Label(frame_card, text="Erro na Imagem", bg="white", fg="red").pack(pady=10)
    print(e)

# 4. Título e Campos
tk.Label(frame_card, text="Acesso ao Sistema", font=("Arial", 12, "bold"), bg="white", fg="#555").pack(pady=5)

frame_inputs = tk.Frame(frame_card, bg="white")
frame_inputs.pack(pady=10)

# CPF
tk.Label(frame_inputs, text="CPF:", bg="white", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
cpf_entry = tk.Entry(frame_inputs, validate="key", validatecommand=(frame_inputs.register(validar_input_cpf), "%P"), width=25)
cpf_entry.grid(row=1, column=0, pady=(0, 10))

# Senha
tk.Label(frame_inputs, text="Senha:", bg="white", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
senha_entry = tk.Entry(frame_inputs, show="*", width=25)
senha_entry.grid(row=3, column=0, pady=(0, 20))

# Botão Entrar
btn_entrar = tk.Button(frame_card, text="ENTRAR", width=20, height=2, 
                       bg=COR_INICIAL, fg="white", font=("Arial", 10, "bold"), 
                       command=tentar_login, cursor="hand2")
btn_entrar.pack(pady=10)

root.mainloop()