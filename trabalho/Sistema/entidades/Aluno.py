from Sistema.bancoDeDados.conexao import criar_conexao


# ---------------- CLASSE ALUNO ---------------- #

class Aluno:
    TABLE = "alunos"

    def __init__(self, id_usuario, curso):
        self.id_usuario = id_usuario
        self.curso = curso


# ---------------- MÉTODOS CRUD ---------------- #

    def criar(self):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            comando = f"""
                INSERT INTO {Aluno.TABLE} (id_usuario, curso)
                VALUES (%s, %s)
            """
            cursor.execute(comando, (self.id_usuario, self.curso))
            conexao.commit()
            return "Aluno cadastrado!"
        except Exception as e:
            return f"Erro ao cadastrar aluno: {e}"
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def ler(condicao="", valores=None, limit=None):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            comando = f"SELECT * FROM {Aluno.TABLE}"
            
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

    def editar(self, id_antigo):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            comando = f"""
                UPDATE {Aluno.TABLE}
                SET id = %s, curso = %s
                WHERE id = %s
            """
            cursor.execute(comando, (self.id, self.curso, id_antigo))
            conexao.commit()
            return "Sucesso ao editar!"
        except Exception as e:
            return f"Ocorreu algo de errado: {e}"
        finally:
            cursor.close()
            conexao.close()

    def deletar(self):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            comando = f"DELETE FROM {Aluno.TABLE} WHERE id = %s"
            cursor.execute(comando, (self.id,))
            conexao.commit()
            return "Sucesso ao deletar!"
        except Exception as e:
            return f"Ocorreu algo de errado: {e}"
        finally:
            cursor.close()
            conexao.close()
