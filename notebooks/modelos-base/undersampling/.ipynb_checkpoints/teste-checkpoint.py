import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
# Caminho para o arquivo Parquet
caminho_arquivo_parquet = 'df_com_falhas_filtered.parquet'

# Carrega o arquivo Parquet em um DataFrame
df = pd.read_parquet(caminho_arquivo_parquet)

# Imprime as primeiras linhas do DataFrame (opcional)


# Imprime o número de linhas no DataFrame
numero_de_linhas = len(df)
print(f'O arquivo Parquet tem {numero_de_linhas} linhas.')

for column in df.columns:
    if pd.isna(df[column].iloc[0]):
        for i in range(1, len(df)):
            if not pd.isna(df[column].iloc[i]):
                df[column].iloc[0] = df[column].iloc[i]
                break

df = df.fillna(method='ffill')

# Crie uma nova coluna 'message_error' que é a soma das colunas 'message0418DAA-1' e 'message0422DAA-1'
df['message_error'] = df['message0418DAA-1'] + df['message0422DAA-1']

# Define uma função para substituir valores
def substituir_valor(valor):
    if valor >= 2:
        return 1
    else:
        return valor

# Use a função apply para substituir valores na coluna 'message_error'
df['message_error'] = df['message_error'].apply(substituir_valor)

# Imprima a coluna 'message_error' após a substituição
print(df['message_error'])

print(df.head())

output_parquet_file = 'df_final'
table = pa.Table.from_pandas(df)
pq.write_table(table, output_parquet_file)
