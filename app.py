import tkinter as tk
from utils import read_tasks, on_closing, add_task, create_task_row

root = tk.Tk(screenName="Todo Tasks")

root.title("Tasks")
root.minsize(500, 600)

tasks = {}
read_tasks('tasks.txt', tasks)

top_frame = tk.Frame(root)
top_frame.pack(padx=5, pady=5, fill='x')
tk.Label(top_frame, text="Tasks to do: ").pack(pady=10, side='left')
add_button = tk.Button(top_frame, text='Add Task', command=lambda r=root, t=tasks: add_task(r, t)).pack(pady=10, side='right')

for task, val in tasks.items(): # make check boxes
    create_task_row(task, val, root, tasks)
    
root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, "tasks.txt", tasks))
root.mainloop()

