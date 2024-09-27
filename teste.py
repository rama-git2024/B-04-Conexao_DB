import pyodbc
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()  # Este comando lê o arquivo .env automaticamente

# Definindo os parâmetros de conexão a partir das variáveis de ambiente
server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

# Verificando se as variáveis foram carregadas corretamente
print(f"Server: {server}")
print(f"Database: {database}")
print(f"Username: {username}")

# String de conexão com os dados lidos do .env
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Conectando ao banco de dados
try:
    conn = pyodbc.connect(connection_string)
    print("Conexão bem-sucedida!")

    # Criando o cursor para executar a consulta
    cursor = conn.cursor()
    
    # Definindo a consulta SQL
    query = """
    SELECT
        ROW_NUMBER() OVER (ORDER BY a.F00230 ASC) AS id_comarca,
        a.F00230 AS comarca,
        a.F00230 AS comarca_ref,
        MAX(b.F00075) AS estado,
        MAX(b.F00074) AS UF
    FROM [ramaprod].[dbo].T00049 AS a
    LEFT JOIN [ramaprod].[dbo].T00023 AS b ON a.F00232 = b.ID
    GROUP BY a.F00230
    ORDER BY a.F00230 ASC
    """ 
    
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
