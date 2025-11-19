from Sistema.bancoDeDados.conexao import criar_conexao


# ---------------- CLASSE NOTA ---------------- #

class Nota:
    TABLE = "notas"

    def __init__(self, disciplina_id, aluno_id, professor_id, nota_trabalho, nota_prova, matricula_id):
        self.disciplina_id = disciplina_id
        self.aluno_id = aluno_id
        self.professor_id = professor_id
        self.nota_trabalho = nota_trabalho
        self.nota_prova = nota_prova
        self.matricula_id = matricula_id


# ---------------- MÉTODOS CRUD ---------------- #

    def criar(self):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            comando = f"""
                INSERT INTO {Nota.TABLE}
                (disciplina_id, aluno_id, professor_id, nota_trabalho, nota_prova, matricula_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(comando, (
                self.disciplina_id,
                self.aluno_id,
                self.professor_id,
                self.nota_trabalho,
                self.nota_prova,
                self.matricula_id
            ))
            conexao.commit()
            return "Nota lançada!"
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
            comando = f"SELECT * FROM {Nota.TABLE}"
            if condicao:
                comando += f" WHERE {condicao}"
            cursor.execute(comando, valores or ())
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    def editar(self, id_nota):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            comando = f"""
                UPDATE {Nota.TABLE}
                SET disciplina_id=%s, aluno_id=%s, professor_id=%s,
                    nota_trabalho=%s, nota_prova=%s, matricula_id=%s
                WHERE id=%s
            """
            cursor.execute(comando, (
                self.disciplina_id,
                self.aluno_id,
                self.professor_id,
                self.nota_trabalho,
                self.nota_prova,
                self.matricula_id,
                id_nota
            ))
            conexao.commit()
            return "Nota atualizada!"
        finally:
            cursor.close()
            conexao.close()
            
        
    @staticmethod
    def deletar(id):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(f"DELETE FROM {Nota.TABLE} WHERE id=%s", (id,))
            conexao.commit()
            return "Nota deletada!"
        finally:
            cursor.close()
            conexao.close()
           
    
# ---------------- MÉTODO DE LEITURA COM JOIN ---------------- #
   
    @staticmethod
    def dadosTabela(condicao="", valores=None):
        conexao = criar_conexao()
        cursor = conexao.cursor()
        try:
            # Consulta SQL com JOIN para buscar todos os nomes relevantes
            comando = """
                SELECT 
                    n.id,                  -- Coluna 0: ID da Nota
                    d.nome AS disciplina_nome, -- Coluna 1: Nome da Disciplina
                    u_aluno.nome AS aluno_nome, -- Coluna 2: Nome do Aluno
                    u_prof.nome AS professor_nome, -- Coluna 3: Nome do Professor
                    n.nota_trabalho,       -- Coluna 4: Nota do Trabalho
                    n.nota_prova,          -- Coluna 5: Nota da Prova
                    (n.nota_trabalho + n.nota_prova) AS media -- Coluna 6: Média (Trabalho + Prova)
                FROM notas AS n
                
                -- JOIN para obter Nome do Aluno
                JOIN alunos AS a ON n.aluno_id = a.id
                JOIN usuarios AS u_aluno ON a.id_usuario = u_aluno.id
                
                -- JOIN para obter Nome do Professor
                JOIN professores AS p ON n.professor_id = p.id
                JOIN usuarios AS u_prof ON p.id_usuario = u_prof.id
                
                -- JOIN para obter Nome da Disciplina
                JOIN disciplinas AS d ON n.disciplina_id = d.id
            """
            
            if condicao:
                # A condição WHERE deve usar os aliases: d.nome, u_aluno.nome, u_prof.nome
                comando += f" WHERE {condicao}"
                
            comando += " ORDER BY u_aluno.nome, d.nome"
            
            cursor.execute(comando, valores or ())
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Erro ao executar dadosTabela na Nota: {e}")
            return []
            
        finally:
            cursor.close()
            conexao.close()