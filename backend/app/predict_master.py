import os
import glob
import pandas as pd
from pycaret.classification import *
from pycaret.classification import load_model

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
predict_file_path = "./predict_file"
predict_file_name = "TCRF_ARCHIVE_06120091_20230526102932.parquet"

df_to_predict = pd.read_parquet(predict_file_path + "/" + predict_file_name)

columns_to_analyze = ["bleedFavTmCmd-1a", "bleedFavTmCmd-1b", "bleedFavTmFbk-1a",
                 "bleedFavTmFbk-1b", "bleedHprsovCmdStatus-1a",
                 "bleedHprsovCmdStatus-1b","bleedHprsovOpPosStatus-1a",
                 "bleedHprsovOpPosStatus-1b","bleedMonPress-1a",
                 "bleedMonPress-1b","bleedOnStatus-1a", "bleedOnStatus-1b",
                 "bleedPrecoolDiffPress-1a", "bleedPrecoolDiffPress-1b",
                 "bleedPrsovClPosStatus-1a","bleedPrsovFbk-1a"]  

df_to_predict = pre_processing(columns_to_analyze, df_to_predict)

df_to_predict = moving_average(df_to_predict, 50_000)

model_1_week = load_model("failure_1_week")

#teste destrutivo
print(model_1_week)

predictions = predict_model(model_1_week, data=df_to_predict, raw_score=True)

print(predictions)

print(predictions.info())

print(predictions["prediction_label"].iloc[-1])
