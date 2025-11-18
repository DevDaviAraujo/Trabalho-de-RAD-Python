import tkinter as tk
from tkinter import messagebox
import importlib.util, os


# ---------------- CARREGANDO AS CLASSES ---------------- #

def carregar_class(nome):
    caminho = os.path.join('Sistema', 'entidades', f'{nome}.py')
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, nome)

Matricula = carregar_class("Matricula")


# ---------------- EXCLUINDO ---------------- #

def janela_excluir(id_matricula, refresh):
    resp = messagebox.askyesno("Excluir", "Deseja realmente excluir esta matrícula?")
    if not resp:
        return
    
    msg = Matricula.deletar(id_matricula)
    messagebox.showinfo("OK", msg)
    refresh()
