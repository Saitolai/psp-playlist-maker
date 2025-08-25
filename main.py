import tkinter as tk
from tkinter import filedialog, messagebox
import os


def add_files():
    files = filedialog.askopenfilenames(
        title="Select music files",
        filetypes=[("Audio files", "*.mp3 *.wav *.flac *.aac"), ("All files", "*.*")]
    )
    for f in files:
        file_list.insert(tk.END, f)


def remove_selected():
    selected = file_list.curselection()
    for i in reversed(selected):
        file_list.delete(i)


def clear_all():
    file_list.delete(0, tk.END)


def move_up():
    selected = file_list.curselection()
    for i in selected:
        if i == 0:
            continue
        text = file_list.get(i)
        file_list.delete(i)
        file_list.insert(i - 1, text)
        file_list.selection_set(i - 1)


def move_down():
    selected = file_list.curselection()
    for i in reversed(selected):
        if i == file_list.size() - 1:
            continue
        text = file_list.get(i)
        file_list.delete(i)
        file_list.insert(i + 1, text)
        file_list.selection_set(i + 1)


def save_playlist():
    if file_list.size() == 0:
        messagebox.showerror("Error", "No files added!")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".m3u8",   # now defaults to m3u8
        filetypes=[("M3U8 Playlist", "*.m3u8"), ("All files", "*.*")]
    )

    if save_path:
        with open(save_path, "w", encoding="utf-8") as playlist:
            for i in range(file_list.size()):
                full_path = file_list.get(i)

                # Try to find the "\MUSIC\" part in the path
                try:
                    rel_index = full_path.upper().rindex("\\MUSIC\\")
                    rel_path = full_path[rel_index:]  # keep everything after \MUSIC\
                except ValueError:
                    rel_path = "\\MUSIC\\" + os.path.basename(full_path)

                playlist.write(rel_path + "\n")

        messagebox.showinfo("Done", f"Playlist saved as:\n{save_path}")


# GUI Setup
root = tk.Tk()
root.title("PSP Playlist Creator")
root.geometry("550x480")

frame = tk.Frame(root)
frame.pack(pady=10)

add_button = tk.Button(frame, text="Add Music Files", command=add_files)
add_button.grid(row=0, column=0, padx=5)

save_button = tk.Button(frame, text="Save Playlist", command=save_playlist)
save_button.grid(row=0, column=1, padx=5)

file_list = tk.Listbox(root, width=70, height=15, selectmode=tk.SINGLE)
file_list.pack(pady=10)

# Controls for reordering
control_frame = tk.Frame(root)
control_frame.pack()

remove_button = tk.Button(control_frame, text="Remove Selected", command=remove_selected)
remove_button.grid(row=0, column=0, padx=5)

up_button = tk.Button(control_frame, text="Move Up", command=move_up)
up_button.grid(row=0, column=1, padx=5)

down_button = tk.Button(control_frame, text="Move Down", command=move_down)
down_button.grid(row=0, column=2, padx=5)

clear_button = tk.Button(control_frame, text="Clear All", command=clear_all)
clear_button.grid(row=0, column=3, padx=5)

root.mainloop()
