import os
import glob
import pandas as pd
from pycaret.classification import *

def get_parquet_files(folder_path):
    # Use glob to find all parquet files in the specified directory
    parquet_files = glob.glob(os.path.join(folder_path, "*.parquet"))

    if not parquet_files:
        print("\nNo parquet files found in the specified directory.")
    else:
        print("\nParquet files in the directory ", folder_path, ":")
        for file_path in parquet_files:
            print(file_path)

    return parquet_files


def pre_processing(selected_columns, dataframe_treat):

    pre_processed_dataframe = pd.DataFrame()
    pre_processed_dataframe = dataframe_treat[selected_columns]

    # change all columns from float64 to float32
    pre_processed_dataframe = pre_processed_dataframe.astype('float32')

    pre_processed_dataframe = pre_processed_dataframe.fillna(0)

    # normalize the data between 0 and 1 for each column #
    #pre_processed_dataframe = pre_processed_dataframe.apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    return pre_processed_dataframe

def moving_average(df_to_average, window_size):

    averaged_dataframe = df_to_average.apply(lambda col: col.rolling(window=window_size).mean(), axis=0)

    averaged_dataframe = averaged_dataframe.dropna()

    return averaged_dataframe


# Defining the paths for the files of failure and non-failure data from 1 week pior to a given failure event [Henrique"s script will generate these files separation]    
failures_1_week_folder_path = "./failures"
non_failures_1_week_folder_path = "./non_failures"

# Call the function to print the parquet files in the specified directories
print("\n Arquivos referentes a falhas: ")
failure_files = get_parquet_files(failures_1_week_folder_path)

print("\n Arquivos referentes a não falhas: ")
non_failure_files = get_parquet_files(non_failures_1_week_folder_path)

columns_to_analyze = ["bleedFavTmCmd-1a", "bleedFavTmCmd-1b", "bleedFavTmFbk-1a",
                 "bleedFavTmFbk-1b", "bleedHprsovCmdStatus-1a",
                 "bleedHprsovCmdStatus-1b","bleedHprsovOpPosStatus-1a",
                 "bleedHprsovOpPosStatus-1b","bleedMonPress-1a",
                 "bleedMonPress-1b","bleedOnStatus-1a", "bleedOnStatus-1b",
                 "bleedPrecoolDiffPress-1a", "bleedPrecoolDiffPress-1b",
                 "bleedPrsovClPosStatus-1a","bleedPrsovFbk-1a"]  


df_media_movel_falhas = pd.DataFrame()
for parquet_file in failure_files:

    df_falha = pd.read_parquet(parquet_file)

    print(df_falha.info())

    print("\nPré-processando arquivo de falha...")
    df_falha = pre_processing(columns_to_analyze, df_falha)
    print("\nInformações do arquivo de falha após o pré-processamento:")
    print(df_falha.info())
    print("\nPrimeiras linhas do arquivo de falha após o pré-processamento:")
    print(df_falha.head(7))

    print("\nCalculando média móvel do arquivo de falha...")
    df_falha = moving_average(df_falha, 50_000)
    print("\nInformações do arquivo de falha após a média móvel")
    print(df_falha.info())
    print("\nPrimeiras linhas do arquivo de falha após a média móvel:")
    print(df_falha.head(7))

    df_media_movel_falhas = pd.concat([df_media_movel_falhas, df_falha], ignore_index=True)


############################################ Etiquetagem ########################################

# Adding a column to the failure dataframe to indicate that the data is from a failure event
print("\nEtiquetando o arquivo de falha...")
df_media_movel_falhas["label"] = [1]*len(df_media_movel_falhas)
print(df_media_movel_falhas.head(7))


############################################## Falha ###########################################

#df_nao_falha = pd.read_parquet("./non_failures/TCRF_ARCHIVE_06120091_20230621220332.parquet")
#print(df_nao_falha.info())

df_media_movel_nao_falhas = pd.DataFrame()
for parquet_file in non_failure_files:

    df_nao_falha = pd.read_parquet(parquet_file)

    print(df_nao_falha.info())

    print("\nPré-processando arquivo de não falha...")
    df_nao_falha = pre_processing(columns_to_analyze, df_nao_falha)
    print("\nInformações do arquivo de não falha após o pré-processamento:")
    print(df_nao_falha.info())
    print("\nPrimeiras linhas do arquivo de não falha após o pré-processamento:")
    print(df_nao_falha.head(7))

    print("\nCalculando média móvel do arquivo de não falha...")
    df_nao_falha = moving_average(df_nao_falha, 50_000)
    print("\nInformações do arquivo de falha após a média móvel:")
    print(df_nao_falha.info())
    print("\nPrimeiras linhas do arquivo de falha após a média móvel:")
    print(df_nao_falha.head(7))

    df_media_movel_nao_falhas = pd.concat([df_media_movel_nao_falhas, df_nao_falha], ignore_index=True)


############################################ Etiquetagem ########################################

# Adding a column to the failure dataframe to indicate that the data is from a failure event
print("\nEtiquetando o arquivo de não falha...")
df_media_movel_nao_falhas["label"] = [0]*len(df_media_movel_nao_falhas)
print(df_media_movel_nao_falhas.head(7))

############################################## Concatenando ###########################################

print("\nConcatenando os arquivos de falha e não falha...")
df_traininig = pd.concat([df_media_movel_falhas, df_media_movel_nao_falhas], ignore_index=True)
print(df_traininig.head(7))
print(df_traininig.tail(7))

############################################## Traininig ###########################################

print("\nTreinando o modelo...")

# Setting up the machine learning model
experiment_model_1_week = setup(df_traininig, target='label')

# Compare and evaluate different models
best_model_1_week = compare_models()

# Create the final model
final_model_1_week = create_model(best_model_1_week)

# Save the final model
print("\nSalvando o modelo...")
save_model(final_model_1_week, model_name='failure_1_week')

print("\n######################## Modelo salvo com sucesso!################################")