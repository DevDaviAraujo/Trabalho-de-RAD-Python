from Sistema.bancoDeDados.conexao import criar_conexao
import importlib.util, os


# ---------------- CARREGANDO OUTRAS CLASSES ---------------- #

def carregar_class(nome):
    caminho = os.path.join('Sistema', 'entidades', f'{nome}.py')
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, nome)

Usuario = carregar_class("Usuario")


# ---------------- CLASSE PROFESSOR ---------------- #

class Professor:
    TABLE = "professores"

    def __init__(self, id_usuario, titulacao, area_atuacao):
        self.id_usuario = id_usuario
        self.titulacao = titulacao
        self.area_atuacao = area_atuacao


# ----------------  MÉTODOS CRUD ---------------- #


    def criar(self):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            comando = f"""
                INSERT INTO {Professor.TABLE} (id_usuario, titulacao, area_atuacao)
                VALUES (%s, %s, %s)
            """
            cursor.execute(comando, (self.id_usuario, self.titulacao, self.area_atuacao))
            conexao.commit()
            return "Professor criado!"
        except Exception as e:
            return f"Erro: {e}"
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def ler(condicao="", valores=None, limit=None):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            comando = f"SELECT * FROM {Professor.TABLE}"
            
            if condicao:
                comando += f" WHERE {condicao}"
            
            if isinstance(limit, int) and limit > 0:
                comando += f" LIMIT {limit}"
            
            cursor.execute(comando, valores or ())
            return cursor.fetchall()
        except Exception as e:
            return f"Algo deu errado: {e}"
        finally:
            cursor.close()
            conexao.close()

    def editar(self, id_prof):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            comando = f"""
                UPDATE {Professor.TABLE}
                SET id_usuario=%s, titulacao=%s, area_atuacao=%s
                WHERE id=%s
            """
            cursor.execute(comando, (self.id_usuario, self.titulacao, self.area_atuacao, id_prof))
            conexao.commit()
            return "Professor atualizado!"
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def deletar(id_prof):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(f"DELETE FROM {Professor.TABLE} WHERE id=%s", (id_prof,))
            conexao.commit()
            return "Professor deletado!"
        finally:
            cursor.close()
            conexao.close()
            
