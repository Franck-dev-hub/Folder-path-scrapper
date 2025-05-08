#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 06/01/2025 by Franck
"""

from pathlib import Path
from tkinter import Tk, filedialog, messagebox
from tkinter import ttk
import tkinter as tk


class FolderPathApp:
    # GUI application to select a folder and save its paths to a file.
    def __init__(self, root):
        self.root = root
        self.root.title("Retrieve Folder and File Paths")
        self.root.geometry("500x250")
        self.root.resizable(False, False)

        self.folder_path = tk.StringVar()
        self.include_files = tk.BooleanVar()

        # Create main UI frame
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Folder selection section
        ttk.Label(self.frame, text="Select a folder:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.folder_path, width=40).grid(
            row=1, column=0, sticky=(tk.W, tk.E)
        )
        ttk.Button(self.frame, text="Browse", command=self.select_folder).grid(
            row=1, column=1, sticky=tk.W
        )

        # Checkbox to include files
        self.checkbox = ttk.Checkbutton(
            self.frame, text="Include files (with extensions)", variable=self.include_files
        )
        self.checkbox.grid(row=2, column=0, sticky=tk.W)

        # Save paths button
        ttk.Button(self.frame, text="Save Paths", command=self.save_paths).grid(
            row=3, column=0, pady=10, sticky=tk.W
        )

        # Status label
        self.status_label = ttk.Label(self.frame, text="", foreground="blue")
        self.status_label.grid(row=4, column=0, columnspan=2, sticky=tk.W)

    def select_folder(self):
        # Open a dialog to select a folder and set its path
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def save_paths(self):
        # Retrieve paths (folders and optionally files) and save them to a text file
        folder = self.folder_path.get()
        if not folder:
            self.status_label.config(text="Please select a folder.", foreground="red")
            return

        # Collect folder paths
        paths = [str(path) for path in Path(folder).rglob('*') if path.is_dir()]

        # Include files with extensions if checkbox is checked
        if self.include_files.get():
            paths += [f"{str(path)} - {path.suffix}" for path in Path(folder).rglob('*') if path.is_file()]

        if not paths:
            self.status_label.config(text="No paths found.", foreground="red")
            return

        # Save the paths to a text file
        save_file = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if save_file:
            with open(save_file, 'w', encoding='utf-8') as file:
                file.write("\n".join(paths))
            messagebox.showinfo("Success", f"Paths saved to: {save_file}")
            self.status_label.config(text="Paths saved successfully.", foreground="green")


if __name__ == "__main__":
    # Initialize and run the application
    root = Tk()
    app = FolderPathApp(root)
    root.mainloop()
