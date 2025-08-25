import tkinter as tk

root = tk.Tk()
root.title("Hello PSP Playlist GUI")
root.geometry("300x200")

label = tk.Label(root, text="If you see this window, Tkinter works!", padx=20, pady=20)
label.pack()

root.mainloop()
