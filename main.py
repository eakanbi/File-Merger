import tkinter as tk
from tkinter import filedialog, messagebox
import filemerger
import pandas as pd
import os

class MyGUI:

    def __init__(self):
        self.selected_files = []  # Store the selected file paths
        self.window = tk.Tk()
        self.window.title("File Merger")
        self.window.geometry("600x400")

        self.create_widgets()
        self.create_menu()

        self.window.mainloop()

    def create_widgets(self):
        self.browse_button = tk.Button(self.window, text="Browse", command=self.browse_files)
        self.browse_button.pack()

        self.instruction_label = tk.Label(self.window, text="Click Browse to select files to merge (Selected files can only have csv extension):")
        self.instruction_label.pack()

        self.file_list = tk.Listbox(self.window, selectmode=tk.MULTIPLE, width=60, height=10)
        self.file_list.pack()

        self.delete_button = tk.Button(self.window, text="Delete", command=self.delete_file)
        self.delete_button.pack()

        self.merge_button = tk.Button(self.window, text="Merge", command=self.merge_selected_files)
        self.merge_button.pack()

        # self.info_text = tk.Text(self.window, height=5, width=60)
        # self.info_text.insert(tk.END, "Selected files can only have xlsx or csv extension.")
        # self.info_text.pack()

        self.status_bar = tk.Label(self.window, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_menu(self):
        self.menu_bar = tk.Menu(self.window)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.window.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.window.config(menu=self.menu_bar)

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        if file_paths:
            self.selected_files.extend(file_paths)
            self.show_selected_files()

    def show_selected_files(self):
        self.file_list.delete(0, tk.END)
        for file_path in self.selected_files:
            file_name = os.path.basename(file_path)
            self.file_list.insert(tk.END, file_name)

    def delete_file(self):
        selected_indices = self.file_list.curselection()
        if selected_indices:
            selected_indices = list(selected_indices)
            selected_indices.sort(reverse=True)
            for index in selected_indices:
                self.file_list.delete(index)
                del self.selected_files[index]

    def merge_selected_files(self):
        if len(self.selected_files) == 0:
            self.status_bar.config(text="No files selected for merge.")
            messagebox.showinfo("Merge Files", "No files selected for merge.")
            return

        merged_df = filemerger.merge_files(self.selected_files)
        if merged_df is not None:
            self.save_file(merged_df)

    @staticmethod
    def merge_files(file_paths):
        dataframes = []
        for file_path in file_paths:
            if file_path.endswith(".xlsx"):
                df = pd.read_excel(file_path, dtype=str)
            elif file_path.endswith(".csv"):
                df = pd.read_csv(file_path, dtype=str)
            else:
                messagebox.showerror("Merge Files", f"Invalid file format for file: {file_path}")
                continue
            dataframes.append(df)

        if len(dataframes) == 0:
            messagebox.showinfo("Merge Files", "No valid files selected for merge.")
            return None

        merged_df = pd.concat(dataframes, ignore_index=True)
        return merged_df

    def save_file(self, data):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                data.to_csv(file_path, index=False)
                self.status_bar.config(text="File saved successfully!")
                messagebox.showinfo("Merge Files", "File saved successfully!")

            except Exception as e:
                self.status_bar.config(text=f"Error occurred while saving the file: {str(e)}")
                messagebox.showerror("Merge Files", f"Error occurred while saving the file: {str(e)}")


if __name__ == "__main__":
    gui = MyGUI()
