import pandas as pd

def merge_files(file_paths):
    dataframes = []
    for file_path in file_paths:
        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path, dtype=str)
        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path, dtype=str)
        else:
            print(f"Invalid file format for file: {file_path}")
            continue
        dataframes.append(df)
    
    if len(dataframes) == 0:
        print("No valid files selected for merge.")
        return None

    merged_df = pd.concat(dataframes, ignore_index=True)
    return merged_df
