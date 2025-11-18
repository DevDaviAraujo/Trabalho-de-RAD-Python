from Sistema.bancoDeDados.conexao import criar_conexao


# ---------------- CLASSE DISCIPLINA ---------------- #

class Disciplina:
    TABLE = "disciplinas"

    def __init__(self, nome, professor_id):
        self.nome = nome
        self.professor_id = professor_id


# ---------------- MÉTODOS CRUD ---------------- #

    def criar(self):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                f"INSERT INTO {Disciplina.TABLE} (nome, professor_id) VALUES (%s, %s)",
                (self.nome, self.professor_id),
            )
            conexao.commit()
            return "Disciplina criada!"
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def ler(condicao="", valores=None):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            comando = f"SELECT * FROM {Disciplina.TABLE}"
            if condicao:
                comando += f" WHERE {condicao}"
            cursor.execute(comando, valores or ())
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    def editar(self, id_disc):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                f"UPDATE {Disciplina.TABLE} SET nome=%s, professor_id=%s WHERE id=%s",
                (self.nome, self.professor_id, id_disc),
            )
            conexao.commit()
            return "Disciplina atualizada!"
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def deletar(id_disc):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(f"DELETE FROM {Disciplina.TABLE} WHERE id=%s", (id_disc,))
            conexao.commit()
            return "Disciplina deletada!"
        finally:
            cursor.close()
            conexao.close()
            
            
# ---------------- MÉTODO DE LEITURA COM JOIN ---------------- #
    
    @staticmethod
    def dadosTabela(condicao="", valores=None):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            # Consulta SQL para unir Disciplinas -> Professores -> Usuários
            comando = """
                SELECT 
                    d.id,                  -- Coluna 0: ID da Disciplina
                    d.nome,                -- Coluna 1: Nome da Disciplina
                    u.nome AS nome_professor -- Coluna 2: Nome do Professor
                FROM disciplinas AS d
                JOIN professores AS p ON d.professor_id = p.id
                JOIN usuarios AS u ON p.id_usuario = u.id
            """
            
            # Adiciona a condição de filtro (WHERE) se existir
            if condicao:
                # Usamos o 'WHERE' e substituímos o nome das tabelas para o JOIN (d, u)
                comando += f" WHERE {condicao}"
                
            # Adiciona a ordenação
            comando += " ORDER BY d.nome"
            
            cursor.execute(comando, valores or ())
            return cursor.fetchall()
            
        except Exception as e:
            # É bom ter um retorno ou log em caso de erro no SQL
            print(f"Erro ao executar dadosTabela: {e}")
            return [] # Retorna lista vazia em caso de falha
            
        finally:
            cursor.close()
            conexao.close()       
            
