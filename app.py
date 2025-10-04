import tkinter as tk
from tkinter import font, messagebox
from utils import read_tasks, on_closing

root = tk.Tk(screenName="Todo Tasks")

root.title("Tasks")
root.minsize(500, 600)

tasks = {}
read_tasks('tasks.txt', tasks)

def cross_out_text(val: tk.IntVar, checkbox: tk.Checkbutton):
    current_font = font.Font(checkbox, checkbox.cget("font"))
    if val.get():
        current_font.configure(overstrike=True)
    else:
        current_font.configure(overstrike=False)
    checkbox.config(font=current_font)

def remove_task(task, checkbox:tk.Checkbutton, button:tk.Button, frame:tk.Frame):
    checkbox.pack_forget()
    button.pack_forget()
    frame.pack_forget()
    del tasks[task]

def add_task():
    popup = tk.Toplevel(root)
    popup.title("Add Task")
    popup.geometry('300x150')

    tk.Label(popup, text="Enter new task: ").pack(pady=10)
    entry = tk.Entry(popup, width=30)
    entry.pack(pady=5)

    def confirm():
        new_task = entry.get().strip()
        tasks[new_task] = tk.IntVar(value=0)
        create_task_row(new_task, tasks[new_task])
        popup.destroy()

    tk.Button(popup, text="Add", command=confirm).pack(pady=10)

def create_task_row(task, val):
    frame = tk.Frame(root)
    frame.pack(fill='x', padx=5, pady=5)

    checkbox = tk.Checkbutton(frame, text=task, variable=val, justify='left')
    cross_out_text(val, checkbox)
    checkbox.config(command=lambda v=val, c=checkbox: cross_out_text(v, c))
    checkbox.pack(side='left', padx=10)

    remove_button = tk.Button(frame, text="Remove Task")
    remove_button.config(command=lambda t=task, c=checkbox, b=remove_button, f=frame: remove_task(t, c, b, f))
    remove_button.pack(side='right', padx=10)


top_frame = tk.Frame(root)
top_frame.pack(padx=5, pady=5, fill='x')
tk.Label(top_frame, text="Tasks to do: ").pack(pady=10, side='left')
add_button = tk.Button(top_frame, text='Add Task', command=add_task).pack(pady=10, side='right')

for task, val in tasks.items(): # make check boxes
    create_task_row(task, val)
    
root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, "tasks.txt", tasks))
root.mainloop()

