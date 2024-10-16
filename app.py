import pyodbc
from dotenv import load_dotenv
import os
import pandas as pd

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()  # Este comando lê o arquivo .env automaticamente

# Definindo os parâmetros de conexão a partir das variáveis de ambiente
server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

# String de conexão com os dados lidos do .env
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

path = r"C:\Users\pedro.cecere\Documents\Projetos\B - Jurídico Varejo\B - 04 - Conexão Banco de Dados\base.csv"

def leitura_banco_de_dados(connection_string):
    df = pd.DataFrame()
    
    try:
        conn = pyodbc.connect(connection_string)
        print("Conexão bem-sucedida!")

        cursor = conn.cursor()
        
        query = """
        SELECT
            c.F13577 AS criado_em,
            a.F31768 AS operacao
        FROM ramaprod.dbo.T01167 AS a
        LEFT JOIN ramaprod.dbo.T00041 AS b ON a.F35050 = b.ID
        LEFT JOIN ramaprod.dbo.T01166 AS c ON a.F13700 = c.ID
        LEFT JOIN ramaprod.dbo.T00003 AS d ON c.F13576 = d.ID
        LEFT JOIN ramaprod.dbo.T01889 AS e ON c.F26866 = e.ID
        LEFT JOIN ramaprod.dbo.T00030 AS f ON e.F26827 = f.ID
        LEFT JOIN ramaprod.dbo.T01859 AS g ON c.F26458 = g.ID
        WHERE 
            a.F31768 IS NOT NULL
        ORDER BY c.F13577 DESC;
        """ 
        
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame.from_records(rows, columns=['criado_em', 'operacao'])

        df['operacao'] = df['operacao'].str.replace(' ', '', regex=True)
        

    except pyodbc.Error as e:
        print("Erro na conexão:", e)

    finally:
        if 'conn' in locals():
            conn.close()
            print("Conexão encerrada.")
    
    return df

def leitura_planilha(path):
    if os.path.exists(path):
        # Lê a planilha CSV
        df_planilha = pd.read_csv(path, encoding='latin1', delimiter=';')
        
        # Remove caracteres não alfanuméricos da coluna 'Nº da Operação'
        df_planilha['operacao'] = df_planilha['Nº da Operação'].str.replace(r'[^a-zA-Z0-9]', '', regex=True)
        
        # Palavras a serem excluídas (cria padrão regex com bordas de palavra)
        palavras_excluir = ['PRONAMPE', 'FGI', 'FOPAG', 'PESE', 'PE']
        padrao_regex = '|'.join([f'\\b{palavra}\\b' for palavra in palavras_excluir])
        
        # Filtra onde 'Nome do Produto' contém as palavras especificadas
        df_governamental = df_planilha[df_planilha['Nome do Produto'].str.contains(padrao_regex, case=False, regex=True, na=False)]
        
        # Salva o resultado filtrado em um arquivo Excel
        df_governamental.to_excel('operacao_governamental.xlsx', index=False)

        # Filtra o df_planilha para retornar apenas as operações que NÃO CONTÊM as palavras especificadas
        df_planilha = df_planilha[~df_planilha['Nome do Produto'].str.contains(padrao_regex, case=False, regex=True, na=False)]
        
        return df_planilha
    else:
        print(f"O arquivo {path} não foi encontrado.")
        return pd.DataFrame()


def valida_base(df_bd, df_planilha):

    df_bd['operacao_final'] = df_bd['operacao']
    df_planilha['operacao_final'] = df_planilha['operacao']

    df_filtrado = df_planilha[~df_planilha['operacao_final'].isin(df_bd['operacao_final'])]

    return df_filtrado

# Exemplo de uso:
df_bd = leitura_banco_de_dados(connection_string)
df_planilha = leitura_planilha(path)

df_nao_cadastradas  = valida_base(df_bd, df_planilha)

# Exibindo o DataFrame resultante do merge
print(df_nao_cadastradas)
df_nao_cadastradas.to_excel('operacoes nao cadastradas.xlsx', index=False)
df_planilha.to_excel('validacao.xlsx', index=False)