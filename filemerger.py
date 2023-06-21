import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def merge_files(file_paths):
    dataframes = []
    for file_path in file_paths:
        if file_path.endswith(".xlsx"):
            try:
                df = pd.read_excel(file_path, dtype=str)
                dataframes.append(df)
            except Exception as e:
                messagebox.showerror("Merge Files", f"Error occurred while reading the file: {str(e)}")
                print(f"Error occurred while reading the file: {str(e)}")

        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path, dtype=str)
            dataframes.append(df)
        else:
            print(f"Invalid file format for file: {file_path}")
            messagebox.showerror("Merge Files", f"Invalid file format for file: {file_path}")
            continue
        dataframes.append(df)
    
    if len(dataframes) == 0:
        print("No valid files selected for merge.")
        messagebox.showinfo("Merge Files", "No valid files selected for merge.")
        return None

    merged_df = pd.concat(dataframes, ignore_index=True)
    return merged_df
