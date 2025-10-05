import tkinter as tk
from tkinter import font

def read_tasks(file_path, tasks):
    with open(file_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        task, val = line.split('":')
        val = int(val.strip())
        task = task[1:]
        tasks[str(task)] = tk.IntVar(value=val)


def on_closing(root:tk.Tk, file_path:str, tasks:dict):
    with open(file_path, "w") as f:
        for task, val in tasks.items():
            line = '"' + task + '"' + ":" + (str(1) if val.get() else str(0)) + "\n"
            f.write(line)
    root.destroy()

def cross_out_text(val: tk.IntVar, checkbox: tk.Checkbutton):
    current_font = font.Font(checkbox, checkbox.cget("font"))
    if val.get():
        current_font.configure(overstrike=True)
    else:
        current_font.configure(overstrike=False)
    checkbox.config(font=current_font)

def remove_task(task, checkbox:tk.Checkbutton, button:tk.Button, frame:tk.Frame, tasks):
    checkbox.pack_forget()
    button.pack_forget()
    frame.pack_forget()
    del tasks[task]

def add_task(root, tasks):
    popup = tk.Toplevel(root)
    popup.title("Add Task")
    popup.geometry('300x150')

    tk.Label(popup, text="Enter new task: ").pack(pady=10)
    entry = tk.Entry(popup, width=30)
    entry.pack(pady=5)

    def confirm(root):
        new_task = entry.get().strip()
        tasks[new_task] = tk.IntVar(value=0)
        create_task_row(new_task, tasks[new_task], root, tasks)
        popup.destroy()

    tk.Button(popup, text="Add", command=lambda r=root: confirm(r)).pack(pady=10)

def create_task_row(task, val, root, tasks):
    frame = tk.Frame(root)
    frame.pack(fill='x', padx=5, pady=5)

    checkbox = tk.Checkbutton(frame, text=task, variable=val, justify='left')
    cross_out_text(val, checkbox)
    checkbox.config(command=lambda v=val, c=checkbox: cross_out_text(v, c))
    checkbox.pack(side='left', padx=10)

    remove_button = tk.Button(frame, text="Remove Task")
    remove_button.config(command=lambda t=task, c=checkbox, b=remove_button, f=frame: remove_task(t, c, b, f, tasks))
    remove_button.pack(side='right', padx=10)