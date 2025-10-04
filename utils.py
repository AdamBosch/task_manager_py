import tkinter as tk

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