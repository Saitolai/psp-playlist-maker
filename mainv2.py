import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from tkinterdnd2 import DND_FILES, TkinterDnD

import webbrowser

import sys
import os

# Optional: set this to your actual MUSIC folder on the PSP card if auto-detect fails
# Example: r"E:\PSP\MUSIC"
MANUAL_MUSIC_ROOT = None  # or set a path string as above

SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac", ".at3", ".oma", ".wma", ".m4a"}

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def to_psp_relpath(full_path: str) -> str:
    r"""Return PSP-style path like \MUSIC\sub\folder\file.mp3"""

    # --- NEW FIX: Skip processing if it is already a PSP path ---
    normalized = full_path.strip().replace("/", "\\")
    if normalized.upper().startswith(r"\MUSIC"):
        return normalized
    # ------------------------------------------------------------

    p = Path(full_path)

    # Try to find the 'MUSIC' segment in the path (case-insensitive)
    parts_lower = [part.lower() for part in p.parts]
    for i, seg in enumerate(parts_lower):
        if seg == "music":
            rel_parts = p.parts[i:]  # keep from MUSIC onward
            return "\\" + "\\".join(rel_parts)

    # If not found, try manual base
    if MANUAL_MUSIC_ROOT:
        try:
            base = Path(MANUAL_MUSIC_ROOT).resolve()
            rel = p.resolve().relative_to(base)
            return "\\MUSIC\\" + str(rel).replace("/", "\\")
        except Exception:
            pass

    # Fallback: just drop under \MUSIC\
    return "\\MUSIC\\" + p.name


def add_files():
    files = filedialog.askopenfilenames(
        title="Select music files",
        filetypes=[("Audio files", "*.mp3 *.wav *.flac *.aac *.at3 *.oma *.wma *.m4a"), ("All files", "*.*")]
    )
    for f in files:
        file_list.insert(tk.END, f)


def remove_selected():
    selected = file_list.curselection()
    
    # Validation 1: Check if anything is actually selected
    if not selected:
        messagebox.showwarning("Selection Error", "No file selected to remove!")
        return

    # Validation 2: Ask for confirmation
    if messagebox.askyesno("Confirm Remove", "Are you sure you want to remove the selected file(s) from the list?"):
        for i in reversed(selected):
            file_list.delete(i)


def clear_all():
    # Validation 1: Check if list is already empty
    if file_list.size() == 0:
        return

    # Validation 2: Ask for confirmation (Critical for "Clear All")
    if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear the ENTIRE playlist?"):
        file_list.delete(0, tk.END)


def move_up():
    selected = file_list.curselection()
    if not selected:
        return

    selected_set = set(selected)
    for i in selected:
        # Don't move if at the very top OR if the item above is also selected and couldn't move
        if i == 0 or (i - 1) in selected_set:
            continue
        text = file_list.get(i)
        file_list.delete(i)
        file_list.insert(i - 1, text)
        file_list.selection_set(i - 1)
        file_list.activate(i - 1)
        selected_set.remove(i)
        selected_set.add(i - 1)

    file_list.see(min(selected_set))


def move_down():
    selected = file_list.curselection()
    if not selected:
        return

    selected_set = set(selected)
    last_index = file_list.size() - 1
    for i in reversed(selected):
        # Don't move if at the very bottom OR if the item below is also selected and couldn't move
        if i == last_index or (i + 1) in selected_set:
            continue
        text = file_list.get(i)
        file_list.delete(i)
        file_list.insert(i + 1, text)
        file_list.selection_set(i + 1)
        file_list.activate(i + 1)
        selected_set.remove(i)
        selected_set.add(i + 1)

    file_list.see(max(selected_set))


def save_playlist():
    if file_list.size() == 0:
        messagebox.showerror("Error", "No files added!")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".m3u8",
        filetypes=[("M3U8 Playlist", "*.m3u8"), ("All files", "*.*")]
    )

    if save_path:
        with open(save_path, "w", encoding="utf-8", newline="\n") as playlist:
            for i in range(file_list.size()):
                full_path = file_list.get(i)
                rel_path = to_psp_relpath(full_path)
                playlist.write(rel_path + "\n")

        messagebox.showinfo("Done", f"Playlist saved as:\n{save_path}")

def load_playlist():
    load_path = filedialog.askopenfilename(
        title="Open PSP Playlist",
        filetypes=[("M3U8 Playlist", "*.m3u8"), ("All files", "*.*")]
    )

    if load_path:
        try:
            with open(load_path, "r", encoding="utf-8") as playlist:
                lines = [line.strip() for line in playlist if line.strip()]
            
            file_list.delete(0, tk.END)  # clear existing list
            for line in lines:
                file_list.insert(tk.END, line)
            
            messagebox.showinfo("Loaded", f"Playlist loaded:\n{load_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load playlist:\n{e}")

def handle_drop(event):
    try:
        # event.data contains the file paths
        files = root.tk.splitlist(event.data)
        for path in files:
            p = Path(path)
            # Check if it's a directory or a file
            if p.is_dir():
                for subfile in sorted(p.rglob("*")):
                    if subfile.is_file() and subfile.suffix.lower() in SUPPORTED_EXTENSIONS:
                        file_list.insert(tk.END, str(subfile))
            elif p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS:
                file_list.insert(tk.END, str(p))
                # print(f"Added file: {path}")
            else:
                print(f"Skipped non-audio or invalid path: {path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def show_about():
    messagebox.showinfo(
        "About PSP Playlist Maker",
        "PSP Playlist Maker V2.1.0\n\n"
        "For SONY PSP music playlists.\n\n"
        "Created by Saitolai\n\n"
        "Icon designed by Tina"
    )

def open_url():
    webbrowser.open(
        "https://github.com/Saitolai/psp-playlist-maker"
    )

def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

# GUI Setup
root = TkinterDnD.Tk()
root.title("PSP Playlist Maker")

try:
    # Use the function to find the icon inside the .exe
    icon_path = resource_path("favicon.ico")
    root.iconbitmap(icon_path)
except Exception:
    pass

root.geometry("560x500")

header_text = tk.Label(
    root,
    text="Welcome to PSP Playlist Maker!",
    font=("Arial", 20),
    fg="#333333"
)

instruction_label = tk.Label(
    root,
    text="Drag and drop music files below\n(or use File > Add Music Files)",
    font=("Arial", 10),
    fg="#333333"
)

# add_button = tk.Button(frame, text="Add Music Files", command=add_files)
# add_button.grid(row=0, column=0, padx=5)

# save_button = tk.Button(frame, text="Save Playlist", command=save_playlist)
# save_button.grid(row=0, column=1, padx=5)

# load_button = tk.Button(frame, text="Load Playlist", command=load_playlist)
# load_button.grid(row=0, column=2, padx=5)

header_text.pack(pady=(0, 0))
instruction_label.pack(pady=(5, 0))

list_frame = tk.Frame(root)
list_frame.pack(pady=5, fill=tk.BOTH, expand=True, padx=15)
scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)

file_list = tk.Listbox(
    list_frame,
    width=70,
    height=20,
    selectmode=tk.EXTENDED,
    yscrollcommand=scrollbar.set
)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=file_list.yview)

# Make the listbox a drop target for files
file_list.drop_target_register(DND_FILES)
file_list.dnd_bind('<<Drop>>', handle_drop)

# Controls for reordering
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

remove_button = tk.Button(control_frame, text="Remove Selected", command=remove_selected)
remove_button.grid(row=0, column=0, padx=5)

up_button = tk.Button(control_frame, text="Move Up", command=move_up)
up_button.grid(row=0, column=1, padx=5)

down_button = tk.Button(control_frame, text="Move Down", command=move_down)
down_button.grid(row=0, column=2, padx=5)

clear_button = tk.Button(control_frame, text="Clear All", command=clear_all)
clear_button.grid(row=0, column=3, padx=5)

menubar = tk.Menu(root)

file_menu = tk.Menu(menubar, tearoff=0)

file_menu.add_command(label="Add Music Files", command=add_files)

file_menu.add_separator()
file_menu.add_command(label="Load Playlist", command=load_playlist)
file_menu.add_command(label="Save Playlist", command=save_playlist)

file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
help_menu.add_separator()
help_menu.add_command(label="PSP Github Repository", command=open_url)

menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menubar)

root.protocol("WM_DELETE_WINDOW", exit_app)

root.mainloop()