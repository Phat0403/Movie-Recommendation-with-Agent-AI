import os
import pandas as pd

def convert_spark_folder_to_csv(input_folder, output_file):
    """
    Convert a folder containing Spark DataFrames to a single CSV file.

    Args:
        input_folder (str): Path to the input folder containing Spark DataFrames.
        output_file (str): Path to the output CSV file.
    """
    df_list = []

    # Iterate over all files in the input folder    
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            # Read the CSV file into a DataFrame
            try:
                df = pd.read_csv(os.path.join(input_folder, filename))
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                raise e
            # Save the DataFrame as a CSV file in the temporary directory
            df_list.append(df)

    # Concatenate all DataFrames into a single DataFrame
    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        # Save the combined DataFrame to a single CSV file
        combined_df.to_csv(output_file, index=False)
    else:
        print(f"No CSV files found in the input folder {input_folder}.")
    
if __name__ == "__main__":
    # input_folder = 'backend/data/new_name_basics'
    # output_file = 'backend/data/new_name_basics.csv'
    
    # convert_spark_folder_to_csv(input_folder, output_file)
    # print(f"Converted Spark folder to CSV file: {output_file}")
    for folder_path in os.listdir('../backend/data'):
        if os.path.isdir(os.path.join('../backend/data', folder_path)):
            try:
                input_folder = os.path.join('../backend/data', folder_path)
                output_file = os.path.join('../backend/data', f"{folder_path}.csv")
                convert_spark_folder_to_csv(input_folder, output_file)
                print(f"Converted Spark folder to CSV file: {output_file}")
            except Exception as e:
                print(f"Error converting {folder_path} to CSV: {e}")
                continue