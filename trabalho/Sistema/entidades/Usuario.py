from Sistema.bancoDeDados.conexao import criar_conexao


# ---------------- CLASSE USUARIO ---------------- #

class Usuario:
    TABLE = "usuarios"

    def __init__(self, cpf, nome, email, senha, tipo):
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo
        

# ---------------- MÉTODOS CRUD ---------------- #

    def criar(self):
        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:
            comando = f"""
                INSERT INTO {Usuario.TABLE} (cpf, nome, email, senha, tipo)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(comando, (self.cpf, self.nome, self.email, self.senha, self.tipo))
            conexao.commit()

            return cursor.lastrowid    # RETORNA O ID GERADO
        except Exception as e:
            return f"Erro ao criar usuário: {e}"
        finally:
            cursor.close()
            conexao.close()


    @staticmethod
    def ler(condicao="", valores=None, limit=None):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            comando = f"SELECT * FROM {Usuario.TABLE}"
            if condicao:
                comando += f" WHERE {condicao}"
            if limit:
                comando += f" LIMIT {limit}"
            cursor.execute(comando, valores or ())
            return cursor.fetchall()
        except Exception as e:
            return f"Erro ao ler: {e}"
        finally:
            cursor.close()
            conexao.close()

    def editar(self, id_usuario):
        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:
            # Se não houver senha → update sem senha
            if not self.senha:
                comando = f"""
                    UPDATE {Usuario.TABLE}
                    SET cpf=%s, nome=%s, email=%s, tipo=%s
                    WHERE id=%s
                """
                valores = (self.cpf, self.nome, self.email, self.tipo, id_usuario)

            else:  # Se houver senha → update com senha
                comando = f"""
                    UPDATE {Usuario.TABLE}
                    SET cpf=%s, nome=%s, email=%s, senha=%s, tipo=%s
                    WHERE id=%s
                """
                valores = (self.cpf, self.nome, self.email, self.senha, self.tipo, id_usuario)

            cursor.execute(comando, valores)
            conexao.commit()
            return "Usuário atualizado!"

        except Exception as e:
            return f"Erro ao editar: {e}"

        finally:
            cursor.close()
            conexao.close()


    @staticmethod
    def deletar(id_usuario):
        conexao = criar_conexao()
        cursor = conexao.cursor()

        try:
            cursor.execute(f"DELETE FROM {Usuario.TABLE} WHERE id=%s", (id_usuario,))
            conexao.commit()
            return "Usuário deletado!"
        except Exception as e:
            return f"Erro ao deletar: {e}"
        finally:
            cursor.close()
            conexao.close()