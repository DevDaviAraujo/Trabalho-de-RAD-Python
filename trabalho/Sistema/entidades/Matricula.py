from Sistema.bancoDeDados.conexao import criar_conexao


# ---------------- CLASSE MATRÍCULA ---------------- #

class Matricula:
    TABLE = "matriculas"

    def __init__(self, aluno_id, disciplina_id):
        self.aluno_id = aluno_id
        self.disciplina_id = disciplina_id


# ---------------- MÉTODOS CRUD ---------------- #

    def criar(self):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                f"INSERT INTO {Matricula.TABLE} (aluno_id, disciplina_id) VALUES (%s, %s)",
                (self.aluno_id, self.disciplina_id),
            )
            conexao.commit()
            return "Matricula criada!"
        except Exception as e:
            return f"Erro: {e}"
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def ler(condicao="", valores=None):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            comando = f"SELECT * FROM {Matricula.TABLE}"
            if condicao:
                comando += f" WHERE {condicao}"
            cursor.execute(comando, valores or ())
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def deletar(id_mat):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(f"DELETE FROM {Matricula.TABLE} WHERE id=%s", (id_mat,))
            conexao.commit()
            return "Matricula deletada!"
        finally:
            cursor.close()
            conexao.close()
             
    
# ---------------- MÉTODO DE LEITURA COM JOIN ---------------- #
   
    @staticmethod
    def dadosTabela(condicao="", valores=None):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            comando = """
                SELECT 
                    m.id,                  -- Coluna 0: ID da Matrícula
                    u.nome AS nome_aluno,  -- Coluna 1: Nome do Aluno
                    d.nome AS nome_disciplina -- Coluna 2: Nome da Disciplina
                FROM matriculas AS m
                
                -- JOIN para obter o NOME do ALUNO
                JOIN alunos AS a ON m.aluno_id = a.id
                JOIN usuarios AS u ON a.id_usuario = u.id
                
                -- JOIN para obter o NOME da DISCIPLINA
                JOIN disciplinas AS d ON m.disciplina_id = d.id
            """
            
            if condicao:
                # O WHERE deve usar os aliases das tabelas (u.nome, d.nome)
                comando += f" WHERE {condicao}"
                
            comando += " ORDER BY u.nome" # Ordena pelo nome do aluno
            
            cursor.execute(comando, valores or ())
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Erro ao executar dadosTabela na Matrícula: {e}")
            return []
            
        finally:
            cursor.close()
            conexao.close()