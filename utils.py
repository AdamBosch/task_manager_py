import tkinter as tk
import os
from tkinter import font, messagebox
from tkinter import ttk

def read_tasks(file_path, tasks):
    with open(file_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        task, val = line.split('":')
        val = int(val.strip())
        task = task[1:]
        tasks[str(task)] = tk.IntVar(value=val)

def read_text(file_path, text_box:tk.Text):
    with open(file_path, 'r') as f:
        text_box.insert("1.0", f.read())


def startup(notebook:ttk.Notebook, tab_list, file_path):

    for dir in os.listdir(file_path):
        text = dir[:-4]
        if dir == "tasks.txt":
            text = "Todo Checklist"
            todo_tab = ttk.Frame(notebook)
            notebook.add(todo_tab, text="Todo Checklist")
            tab_list.append(todo_tab)
        else:
            new_tab = ttk.Frame(notebook)
            tab_list.append(new_tab)
            notebook.add(new_tab, text=text)

    # Create the tabs
    for tab in tab_list:
        tab_name = notebook.tab(tab, 'text')
        text = True
        if tab_name == "Todo Checklist":
            text = False
        create_tab(tab, tab_name, text, exists=True, file_path='data/'+tab_name+'.txt')

    return notebook, tab_list, todo_tab


def on_closing(root:tk.Tk, file_path:str, notebook:ttk.Notebook, tasks:dict):
    filelist = [ f for f in os.listdir(file_path) if f.endswith(".txt") ]
    for f in filelist:
        os.remove(os.path.join(file_path, f))

    for tab_id in notebook.tabs():
        tab_name = notebook.tab(tab_id, 'text')
        tab_widget = notebook.nametowidget(tab_id)

        # Todo Checklist
        if tab_name == "Todo Checklist":
            save_path = os.path.join(file_path, "tasks.txt")
            with open(save_path, "w", encoding="utf-8") as f:
                for task, val in tasks.items():
                    f.write(f'"{task}":{1 if val.get() else 0}\n')

        else:
            # Text tabs
            text_widgets = [child for child in tab_widget.winfo_children() if isinstance(child, tk.Text)]
            if text_widgets:
                text_widget = text_widgets[0]
                content = text_widget.get("1.0", tk.END).strip()
                save_path = os.path.join(file_path, f"{tab_name}.txt")
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(content)
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

def create_tab(tab, text_var, text=True, exists=False, file_path=None):
    label = ttk.Label(tab, text=text_var)
    label.pack(padx=20, pady=20)
    if text:
        input_text_area = tk.Text(tab, wrap='word', background='white', foreground='black')
        input_text_area.pack(fill='both', expand=True, padx=10, pady=10)

        if exists:
            read_text(file_path, input_text_area)

def tab_creator(tab_list, parent, notebook):
    popup = tk.Toplevel(parent)
    popup.title("Create Tab")
    popup.geometry('300x150')
    popup.resizable(False, False)

    tk.Label(popup, text="Enter tab name:").pack(pady=10)
    entry = tk.Entry(popup, width=30)
    entry.pack(pady=5)

    def confirm():
        tab_name = entry.get().strip()
        if not tab_name:
            messagebox.showerror("Error", "Tab name cannot be empty.")
            return

        # Create new tab
        new_tab = ttk.Frame(notebook)
        notebook.add(new_tab, text=tab_name)
        create_tab(new_tab, tab_name)

        tab_list.append(new_tab)
        notebook.select(new_tab)  # Focus on new tab
        popup.destroy()

    tk.Button(popup, text="Add Tab", command=confirm).pack(pady=10)

def remove_tab(notebook:ttk.Notebook):
    selected_tab = notebook.select()
    if notebook.tab(selected_tab, 'text') == "Todo Checklist" or notebook.tab(selected_tab, 'text') == "Ideas":
        messagebox.showerror("Error", "Cannot delete this tab")
        return
    notebook.forget(notebook.select())
