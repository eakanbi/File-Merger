import tkinter as tk
from tkinter import filedialog
import filemerger


selected_files = []  # Store the selected file paths
file_list = None  # Global variable for the file list

def browse_files():
    global selected_files
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        selected_files.extend(file_paths)  # Update the selected file paths
        show_selected_files()

def show_selected_files():
    global selected_files, file_list
    file_list.delete(0, tk.END)  # Clear the file list
    for file_path in selected_files:
        file_list.insert(tk.END, file_path)  # Display the file path in the listbox

def delete_file():
    global selected_files, file_list
    selected_indices = file_list.curselection()  # Get the selected indices
    if selected_indices:
        selected_indices = list(selected_indices)  # Convert to a list
        selected_indices.sort(reverse=True)  # Sort in reverse order to delete from the end
        for index in selected_indices:
            file_list.delete(index)  # Delete from the listbox
            del selected_files[index]  # Delete from the selected_files list

def merge_selected_files():
    global selected_files
    merged_df = filemerger.merge_files(selected_files)
    if merged_df is not None:
        save_file(merged_df)

def save_file(data):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv")
    if file_path:
        try:
            data.to_csv(file_path, index=False)
            print("File saved successfully!")
        except Exception as e:
            print("Error occurred while saving the file:", str(e))

def create_gui():
    global file_list  # Declare file_list as a global variable

    # Create the application window
    window = tk.Tk()

    # Set the window title
    window.title("File Merger")

    # Set the window size
    window.geometry("600x400")

    # Create the browse button
    browse_button = tk.Button(window, text="Browse", command=browse_files)
    browse_button.pack()

    # Set instructions
    instruction_label = tk.Label(window, text="Click Browse to select files to merge (Selected files can only have excel or csv extension):")
    instruction_label.pack()

    # Create the file list
    file_list = tk.Listbox(window, selectmode=tk.MULTIPLE, width=60, height=10)
    file_list.pack()

    # Create the delete button
    delete_button = tk.Button(window, text="Delete", command=delete_file)
    delete_button.pack()

    # Create the merge button
    merge_button = tk.Button(window, text="Merge", command=merge_selected_files)
    merge_button.pack()

    info_text = tk.Text(window, height=5, width=60)
    info_text.insert(tk.END, "Selected files can only have excel or csv extension.")
    info_text.pack()

    # Menu
    menu_bar = tk.Menu(window)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Exit", command=window.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)
    window.config(menu=menu_bar)

    # Status Bar
    status_bar = tk.Label(window, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # Run the application
    window.mainloop()

if __name__ == "__main__":
    create_gui()