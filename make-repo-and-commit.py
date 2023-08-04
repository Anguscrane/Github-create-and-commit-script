import tkinter as tk
from tkinter import messagebox
from github import Github
from tkinter import filedialog
import os
import subprocess

def browse_folder():
    folder_path = filedialog.askdirectory()
    entry_folder_path.delete(0, tk.END)
    entry_folder_path.insert(tk.END, folder_path)

def create_repo_and_push():
    access_token = entry_token.get().strip()
    folder_path = entry_folder_path.get().strip()
    repo_name = entry_repo_name.get().strip()

    try:
        # Authenticate to GitHub using the provided access token
        g = Github(access_token)

        # Get the authenticated user (you can also provide a specific organization name)
        user = g.get_user()

        # Create a new repository on GitHub
        repo = user.create_repo(repo_name)

        # Initialize a new git repository in the folder
        subprocess.run(["git", "init"], cwd=folder_path)

        # Add all files to the git repository
        subprocess.run(["git", "add", "."], cwd=folder_path)

        # Commit the changes
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=folder_path)

        # Set the remote origin to the newly created GitHub repository
        remote_url = repo.clone_url.replace("https://", f"https://{access_token}@")
        subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=folder_path)

        # Push the files to GitHub
        subprocess.run(["git", "push", "-u", "origin", "master"], cwd=folder_path)

        messagebox.showinfo("Success", "Repository created and files pushed to GitHub successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("GitHub Repository Creator")

# GitHub Access Token
label_token = tk.Label(root, text="GitHub Access Token:")
label_token.pack()
entry_token = tk.Entry(root, show="*")
entry_token.pack()

# Repository Name
label_repo_name = tk.Label(root, text="Repository Name:")
label_repo_name.pack()
entry_repo_name = tk.Entry(root)
entry_repo_name.pack()

# Folder Path
label_folder_path = tk.Label(root, text="Folder Path:")
label_folder_path.pack()
entry_folder_path = tk.Entry(root)
entry_folder_path.pack(side=tk.LEFT)
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.pack(side=tk.LEFT)

# Create and Push Button
push_button = tk.Button(root, text="Create Repo and Push", command=create_repo_and_push)
push_button.pack()

root.mainloop()
