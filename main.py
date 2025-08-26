import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

# Optional: set this to your actual MUSIC folder on the PSP card if auto-detect fails
# Example: r"E:\PSP\MUSIC"
MANUAL_MUSIC_ROOT = None  # or set a path string as above

def to_psp_relpath(full_path: str) -> str:
    """Return PSP-style path like \MUSIC\sub\folder\file.mp3"""
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


# GUI Setup
root = tk.Tk()
root.title("PSP Playlist Creator")
root.geometry("560x500")

frame = tk.Frame(root)
frame.pack(pady=10)

add_button = tk.Button(frame, text="Add Music Files", command=add_files)
add_button.grid(row=0, column=0, padx=5)

save_button = tk.Button(frame, text="Save Playlist", command=save_playlist)
save_button.grid(row=0, column=1, padx=5)

file_list = tk.Listbox(root, width=72, height=16, selectmode=tk.SINGLE)
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
