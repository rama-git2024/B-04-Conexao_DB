import pyodbc

# Definindo os parâmetros de conexão
server = '200.155.159.70,1441'        # Nome do servidor SQL Server
database = 'ramaprod' # Nome do banco de dados
username = 'acessoRamaBIFinanceiro'        # Nome de usuário
password = 'uJENTM2MsUGbiJVTDGUQjpFZR5KrmiM'          # Senha

# String de conexão
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Conectando ao banco de dados
try:
    conn = pyodbc.connect(connection_string)
    print("Conexão bem-sucedida!")

    # Criando o cursor para executar a consulta
    cursor = conn.cursor()
    
    # Definindo a consulta SQL
    query = 'SELECT TOP 100 ID FROM dbo.T00041'  # Substitua SUA_TABELA pelo nome da tabela que deseja consultar
    
    # Executando a consulta
    cursor.execute(query)
    
    # Buscando os resultados
    rows = cursor.fetchall()
    
    # Exibindo os resultados
    for row in rows:
        print(row)

except pyodbc.Error as e:
    print("Erro na conexão:", e)

finally:
    # Fechando a conexão
    if 'conn' in locals():
        conn.close()
        print("Conexão encerrada.")
