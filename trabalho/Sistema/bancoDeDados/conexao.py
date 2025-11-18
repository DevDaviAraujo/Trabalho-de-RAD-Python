import mysql.connector

def criar_conexao():
    
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="trabalho"
        )
        return conexao
        
    except Exception as e:
        return f'Ocorreu um erro: {e}'   