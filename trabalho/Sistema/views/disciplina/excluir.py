import tkinter as tk
from tkinter import messagebox
import os, importlib.util


# ---------------- CARREGANDO AS CLASSES ---------------- #

def carregar_class(nome):
    caminho = os.path.join('Sistema', 'entidades', f'{nome}.py')
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, nome)

Disciplina = carregar_class("Disciplina")


# ---------------- EXCLUINDO ---------------- #

def janela_excluir(id_disciplina, reload_callback):
    resp = messagebox.askyesno("Excluir", "Deseja excluir esta disciplina?")
    if not resp:
        return

    msg = Disciplina.deletar(id_disciplina)
    messagebox.showinfo("OK", msg)
    reload_callback()
