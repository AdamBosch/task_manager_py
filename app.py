import tkinter as tk
from tkinter import ttk
from utils import read_tasks, on_closing, add_task, create_task_row, create_tab, tab_creator, remove_tab, startup

def main():
    parent = tk.Tk(screenName="Better Notepad")

    parent.title("Better Notepad")
    parent.minsize(500, 600)
    notebook = ttk.Notebook(parent)

    menu_bar = tk.Menu(parent)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label='File', menu=file_menu)

    tab_list = []

    file_menu.add_command(label='New Tab', command=lambda tl=tab_list, f=parent, n=notebook: tab_creator(tl, f, n))
    file_menu.add_command(label="Delete Tab", command=lambda: remove_tab(notebook))
    parent.config(menu=menu_bar)    

    notebook, tab_list, todo_tab = startup(notebook, tab_list, "data/")

    notebook.pack(padx=10, pady=10, fill="both", expand=True)
    
    tasks = {}
    read_tasks('data/tasks.txt', tasks)


    top_frame = tk.Frame(todo_tab)

    top_frame.pack(padx=5, pady=5, fill='x')
    tk.Label(top_frame, text="Tasks to do: ").pack(pady=10, side='left')
    add_button = tk.Button(top_frame, text='Add Task', command=lambda r=todo_tab, t=tasks: add_task(r, t)).pack(pady=10, side='right')

    for task, val in tasks.items(): # make check boxes
        create_task_row(task, val, todo_tab, tasks)
        
    parent.protocol("WM_DELETE_WINDOW", lambda: on_closing(parent, "data/", notebook, tasks))
    parent.mainloop()

if __name__ == "__main__":
    main()
