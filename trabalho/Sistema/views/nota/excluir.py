# excluirNota.py
import tkinter as tk
from tkinter import messagebox
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
    

# ---------------- EXCLUINDO ---------------- #

def janela_excluir(id_nota, recarregar):
    resposta = messagebox.askyesno("Confirmação", "Deseja excluir esta nota?")
    if not resposta:
        return

    msg = Nota.excluir(id_nota)
    messagebox.showinfo("Resultado", msg)
    recarregar()
