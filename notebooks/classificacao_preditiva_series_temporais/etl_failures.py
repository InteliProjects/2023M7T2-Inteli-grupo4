# Importing from the necessary libraries
import pandas as pd
from pycaret.classification import *

# Function to calculate the moving average for specific columns in a DataFrame
def moving_average(df, column_names, window_size):
    """
    Calculate the moving average for specified columns in a DataFrame.

    Parameters:
    - df: pandas DataFrame
        The input DataFrame.
    - column_names: list of str
        The column names for which moving averages will be calculated.
    - window_size: int
        The size of the moving average window.

    Returns:
    - pandas DataFrame
        A new DataFrame with the same columns as the input, including moving average columns.
    """
    result_df =  pd.DataFrame()

    # Calculate moving averages for each specified column
    for column in column_names:
        result_df[f'{column}_moving_avg'] = df[column].rolling(window=window_size).mean()

    result_df.dropna(inplace=True)
    result_df.reset_index(drop=True, inplace=True)

    return result_df

# Function to generate one dataframe with the moving average for all the files in a given folder
def dataframe_moving_average(file_names, column_names, window_size):
    
    moving_average_total_df = pd.DataFrame()
    
    for file_name in file_names:
        
        temp_dataframe = pd.read_parquet(file_name)
    
        moving_average_temp_dataframe = moving_average(temp_dataframe, column_names, window_size)
    
        print(file_name)
        print(moving_average_temp_dataframe.head(3))
        print("-------------------------------------------------------------------------------\n")
    
        moving_average_total_df = pd.concat([moving_average_total_df, moving_average_temp_dataframe], ignore_index=True)
    
        return moving_average_total_df
    

# Defining the paths for the files of failure and non-failure data from 1 week pior to a given failure event [Henrique's script will generate these files separation]    
failures_1_week_folder_path = "./failures"
non_failures_1_week_folder_path = "./non_failures"
    
# Parameters for generating the dataframes with moving averages for the failure data
failure_files = ["falha_1.parquet", "falha_2.parquet", "falha_3.parquet"]
failure_column_names = ["sensor_1",	"sensor_2",	"sensor_3",	"sensor_4",	"sensor_5",	"sensor_6",	"sensor_7",	"sensor_8"]
window_size = 500_000

# Aplying the function to generate the dataframe with the moving average for the failure data
total_failure_moving_average = dataframe_moving_average(failure_files, failure_column_names, window_size)

# Inspection of the results for the failure data moving average dataframe
print(total_failure_moving_average.head(3))
print(total_failure_moving_average.info())

# Parameters for generating the dataframes with moving averages for the non failure data
non_failure_files = ["nao_falha_1.parquet", "nao_falha_2.parquet", "nao_falha_3.parquet"]
non_failure_column_names = ["sensor_1",	"sensor_2",	"sensor_3",	"sensor_4",	"sensor_5",	"sensor_6",	"sensor_7",	"sensor_8"]
window_size = 500_000

# Aplying the function to generate the dataframe with the moving average for the non failure data
total_non_failure_moving_average = dataframe_moving_average(non_failure_files, non_failure_column_names, window_size)

# Inspection of the results for the failure data moving average dataframe
print(total_non_failure_moving_average.head(3))
print(total_non_failure_moving_average.info())

# Adding a column to the failure dataframe to indicate that the data is from a failure event
total_failure_moving_average["label"] = [1]*len(total_non_failure_moving_average)
print(total_failure_moving_average.head(7))

# Adding a column to the non failure dataframe to indicate that the data is from a non failure event
total_non_failure_moving_average["label"] = [0]*len(total_non_failure_moving_average)
print(total_non_failure_moving_average.head(7))

# Concatenating the failure and non failure dataframes to create the training dataframe to be used in the machine learning model
trainning_df = pd.concat([total_failure_moving_average, total_non_failure_moving_average], ignore_index=True)

# Inspection of the results for the training dataframe (check for 1s at the beginning and 0s at the end of the label column)
print(trainning_df.head(7)) 
print(trainning_df.tail(7))

# Setting up the machine learning model
experiment_model_1_week = setup(trainning_df, target='label')

# Compare and evaluate different models
best_model_1_week = compare_models()

# Create the final model
final_model_1_week = create_model(best_model_1_week)

# Save the final model
save_model(final_model_1_week, model_name='failure_1_week', model_only=True)