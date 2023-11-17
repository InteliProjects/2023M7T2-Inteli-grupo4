import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

def verifica_falhas(df):
    columns_to_check = ['message0418DAA-1', 'message0422DAA-1']
    for column in columns_to_check:
        if any(df[column].nunique() > 1 for value in df[column] if not (value == 0 or pd.isna(value))):
            return True
    return False

falhas = []
num_arquivos_processados = 0  # Variável para contar o número de arquivos processados

def processar_arquivos(root):
    global num_arquivos_processados  # Declara a variável como global
    for arquivo in arquivos:
        arquivo_path = os.path.join(root, arquivo)
        num_arquivos_processados += 1  # Incrementa o contador de arquivos
        print(f"Arquivos processados: {num_arquivos_processados}")
        df_read = pd.read_parquet(arquivo_path, engine='auto')
        if verifica_falhas(df_read):
            falhas.append(arquivo)

for root, _, arquivos in os.walk('./dataset/06120020'):
    print(f"Processando diretório: {root}")
    processar_arquivos(root)

# Imprime a mensagem apenas se não houver arquivos com falhas
if not falhas:
    print("Não foram encontrados arquivos com falhas.")
else:
    print(f"Arquivos com falhas: {falhas}")


#Arquivos com falha no 18:
#Arquivos com falhas: ['TCRF_ARCHIVE_06120018_20220613150340.parquet', 'TCRF_ARCHIVE_06120018_20220615111101.parquet', 'TCRF_ARCHIVE_06120018_20230102035947.parquet', 'TCRF_ARCHIVE_06120018_20230102145838.parquet', 'TCRF_ARCHIVE_06120018_20230529111801.parquet', 'TCRF_ARCHIVE_06120018_20230529111802.parquet', 'TCRF_ARCHIVE_06120018_20230529111803.parquet', 'TCRF_ARCHIVE_06120018_20230529181738.parquet', 'TCRF_ARCHIVE_06120018_20230530173938.parquet', 'TCRF_ARCHIVE_06120018_20230531131402.parquet', 'TCRF_ARCHIVE_06120018_20230531155039.parquet', 'TCRF_ARCHIVE_06120018_20230531180237.parquet', 'TCRF_ARCHIVE_06120018_20230531195638.parquet', 'TCRF_ARCHIVE_06120018_20230531223738.parquet', 'TCRF_ARCHIVE_06120018_20230601013839.parquet', 'TCRF_ARCHIVE_06120018_20230601141301.parquet', 'TCRF_ARCHIVE_06120018_20230601141302.parquet', 'TCRF_ARCHIVE_06120018_20230602190601.parquet', 'TCRF_ARCHIVE_06120018_20230602190604.parquet', 'TCRF_ARCHIVE_06120018_20230602190605.parquet']
#Arquivos com falha no 20:
#Arquivos com falhas: ['TCRF_ARCHIVE_06120020_20230510212802.parquet', 'TCRF_ARCHIVE_06120020_20230605030437.parquet', 'TCRF_ARCHIVE_06120020_20230605194105.parquet', 'TCRF_ARCHIVE_06120020_20230616164139.parquet', 'TCRF_ARCHIVE_06120020_20230709200236.parquet']