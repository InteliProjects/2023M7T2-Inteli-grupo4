import pandas as pd
import os
import warnings
import shutil
from datetime import datetime
import pyarrow as pa
import pyarrow.parquet as pq

warnings.filterwarnings('ignore')

# Caminho completo para o arquivo zip local
zip_file_path = '06120091.zip'  # Substitua pelo caminho real do arquivo

# Caminho onde os dados serão descompactados
output_folder = './dataset'  # Substitua pelo caminho onde você deseja descompactar os dados

# Descompactar os dados
shutil.unpack_archive(zip_file_path, output_folder)

print("Arquivo descompactado com sucesso!")

# Filtro de colunas gerado pelo muricola
# Filtro para as colunas que estão descritas no TAPI - by: muricola

filtered_cols = [
'phaseOfFlight-1',
                'bleedFavTmCmd-1a', 'bleedFavTmCmd-1b',
                'bleedFavTmCmd-2a', 'bleedFavTmCmd-2b', 'bleedFavTmFbk-1a',
                'bleedFavTmFbk-1b', 'bleedFavTmFbk-2b', 'bleedHprsovCmdStatus-1a',
                'bleedHprsovCmdStatus-1b', 'bleedHprsovCmdStatus-2a',
                'bleedHprsovCmdStatus-2b', 'bleedHprsovOpPosStatus-1a',
                'bleedHprsovOpPosStatus-1b', 'bleedHprsovOpPosStatus-2a',
                'bleedHprsovOpPosStatus-2b', 'bleedMonPress-1a',
                'bleedMonPress-1b', 'bleedMonPress-2a', 'bleedMonPress-2b',
                'bleedOnStatus-1a', 'bleedOnStatus-1b', 'bleedOnStatus-2b',
                'bleedPrecoolDiffPress-1a', 'bleedPrecoolDiffPress-1b',
                'bleedPrecoolDiffPress-2a', 'bleedPrecoolDiffPress-2b',
                'bleedPrsovClPosStatus-1a', 'bleedPrsovClPosStatus-2a',
                'bleedPrsovFbk-1a','message0418DAA-1', 'message0422DAA-1'
]

def convert_columns(df_filtered):
    for coluna in df_filtered.columns:
        if df_filtered[coluna].dtype == 'float64':
            df_filtered[coluna] = df_filtered[coluna].astype('float32')

        if df_filtered[coluna].dtype == 'int64':
            df_filtered[coluna] = df_filtered[coluna].astype('int32')

    return df_filtered

def verifica_falhas(df):
    columns_to_check = ['message0418DAA-1', 'message0422DAA-1']
    for column in columns_to_check:
        if any(df[column].nunique() > 1 for value in df[column] if not (value == 0 or pd.isna(value))):
            return True
    return False

falhas = []
dataframes_com_falhas = []  # Lista para armazenar DataFrames com falhas

def processar_arquivos(root, filtered_cols):
    for arquivo in arquivos:
        arquivo_path = os.path.join(root, arquivo)
        df_read = pd.read_parquet(arquivo_path, engine='auto')
        df_filtered = df_read[filtered_cols]
        df_converted = convert_columns(df_filtered)
        dataframes_com_falhas.append(df_converted)
        if verifica_falhas(df_converted):
            falhas.append(arquivo)

for root, _, arquivos in os.walk('./dataset/06120091'):
    processar_arquivos(root, filtered_cols)

# Combinar todos os DataFrames com falhas em um único DataFrame
df_com_falhas = pd.concat(dataframes_com_falhas, ignore_index=True)

# Substituir a contagem de linhas com valores acima de 0
count_above_zero = (df_com_falhas['message0418DAA-1'] > 0).sum()

# Remover todas as linhas com valor 0.0 na coluna 'message0418DAA-1'
df_com_falhas = df_com_falhas[df_com_falhas['message0418DAA-1'] != 0.0]

# Substituir a contagem de linhas com valores NaN
count_nan_or_zero = df_com_falhas['message0418DAA-1'].isna().sum()

if count_nan_or_zero > count_above_zero:
    # Calcule o número de linhas a serem removidas
    num_to_remove = count_nan_or_zero - count_above_zero

    # Encontre os índices das linhas com valor NaN na coluna 'message0418DAA-1'
    indices_to_remove = df_com_falhas[df_com_falhas['message0418DAA-1'].isna()].index

    # Remova as primeiras 'num_to_remove' linhas com valor NaN
    df_com_falhas = df_com_falhas.drop(indices_to_remove[:num_to_remove])

    # Atualize a contagem de linhas com valores NaN
    count_nan_or_zero = df_com_falhas['message0418DAA-1'].isna().sum()

    # Imprima informações sobre a remoção
    print(f'Removeu {num_to_remove} linhas com valor NaN. Total de linhas restantes: {len(df_com_falhas)}')

# Imprimir a quantidade de valores acima de 0 e valores NaN após a retirada
print("Quantidade de valores acima de 0 na coluna 'message0418DAA-1':", count_above_zero)
print("Quantidade de valores NaN na coluna 'message0418DAA-1' após a retirada:", count_nan_or_zero)
output_parquet_file = 'df_com_falhas_filtered.parquet'
table = pa.Table.from_pandas(df_com_falhas)
pq.write_table(table, output_parquet_file)

print(f'DataFrame resultante salvo em {output_parquet_file}')