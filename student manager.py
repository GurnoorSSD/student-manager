import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "students.json"

# ----------------- LOAD OR INIT -----------------
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        students = json.load(f)
else:
    students = []

# ----------------- HELPER FUNCTIONS -----------------
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=2)

def refresh_tree(filtered_students=None):
    for row in tree.get_children():
        tree.delete(row)
    display_students = filtered_students if filtered_students is not None else students
    for i, s in enumerate(display_students):
        color = "#f0f0ff" if i % 2 == 0 else "#ffffff"
        tree.insert("", tk.END, values=(s["roll"], s["name"], s["age"], s["grade"]), tags=('row',))
        tree.tag_configure('row', background=color)

def add_student():
    name = entry_name.get().strip()
    roll = entry_roll.get().strip()
    age = entry_age.get().strip()
    grade = entry_grade.get().strip()
    
    if not (name and roll and age and grade):
        messagebox.showwarning("Input Error", "All fields are required")
        return
    
    for s in students:
        if s["roll"] == roll:
            messagebox.showerror("Duplicate", "Roll number already exists!")
            return

    students.append({"name": name, "roll": roll, "age": age, "grade": grade})
    save_data()
    refresh_tree()
    clear_entries()

def delete_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Select a student to delete")
        return
    roll = tree.item(selected[0])["values"][0]
    global students
    students = [s for s in students if s["roll"] != roll]
    save_data()
    refresh_tree()
    clear_entries()
    btn_update.config(state=tk.DISABLED)
    btn_delete.config(state=tk.DISABLED)

def search_student(event=None):
    term = entry_search.get().strip().lower()
    filtered = [s for s in students if term in s["name"].lower() or term == s["roll"]]
    refresh_tree(filtered)

def update_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Select a student to update")
        return
    roll = tree.item(selected[0])["values"][0]
    
    name = entry_name.get().strip()
    new_roll = entry_roll.get().strip()
    age = entry_age.get().strip()
    grade = entry_grade.get().strip()
    
    if not (name and new_roll and age and grade):
        messagebox.showwarning("Input Error", "All fields are required")
        return
    
    for s in students:
        if s["roll"] == new_roll and s["roll"] != roll:
            messagebox.showerror("Duplicate", "Roll number already exists!")
            return
    
    for s in students:
        if s["roll"] == roll:
            s["name"] = name
            s["roll"] = new_roll
            s["age"] = age
            s["grade"] = grade
            break
    
    save_data()
    refresh_tree()
    clear_entries()
    btn_update.config(state=tk.DISABLED)
    btn_delete.config(state=tk.DISABLED)

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_roll.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_grade.delete(0, tk.END)

def select_student(event):
    selected = tree.selection()
    if not selected:
        btn_update.config(state=tk.DISABLED)
        btn_delete.config(state=tk.DISABLED)
        return
    btn_update.config(state=tk.NORMAL)
    btn_delete.config(state=tk.NORMAL)
    
    s = tree.item(selected[0])["values"]
    entry_roll.delete(0, tk.END)
    entry_roll.insert(0, s[0])
    entry_name.delete(0, tk.END)
    entry_name.insert(0, s[1])
    entry_age.delete(0, tk.END)
    entry_age.insert(0, s[2])
    entry_grade.delete(0, tk.END)
    entry_grade.insert(0, s[3])

# ----------------- GUI -----------------
root = tk.Tk()
root.title("Colorful Student Manager")
root.geometry("750x550")

# Make main background colorful
colors = ["#FFDEE9", "#B5FFFC", "#FFFFBA", "#C2F0C2", "#E0BBE4"]
root.config(bg=colors[0])  # Set a base color

# ----------------- Helper to set frame backgrounds -----------------
def set_frame_color(frame, index):
    frame.config(bg=colors[index % len(colors)])
    for widget in frame.winfo_children():
        try:
            widget.config(bg=colors[index % len(colors)])
        except:
            pass

# Input Frame
frame_input = tk.Frame(root, pady=10)
frame_input.pack(pady=10, fill=tk.X)
set_frame_color(frame_input, 1)

tk.Label(frame_input, text="Name").grid(row=0, column=0, padx=5)
entry_name = tk.Entry(frame_input)
entry_name.grid(row=0, column=1, padx=5)

tk.Label(frame_input, text="Roll").grid(row=0, column=2, padx=5)
entry_roll = tk.Entry(frame_input)
entry_roll.grid(row=0, column=3, padx=5)

tk.Label(frame_input, text="Age").grid(row=1, column=0, padx=5)
entry_age = tk.Entry(frame_input)
entry_age.grid(row=1, column=1, padx=5)

tk.Label(frame_input, text="Grade").grid(row=1, column=2, padx=5)
entry_grade = tk.Entry(frame_input)
entry_grade.grid(row=1, column=3, padx=5)

btn_add = tk.Button(frame_input, text="Add Student", command=add_student)
btn_add.grid(row=2, column=0, columnspan=2, pady=5)
btn_update = tk.Button(frame_input, text="Update Selected", command=update_student, state=tk.DISABLED)
btn_update.grid(row=2, column=2, columnspan=2, pady=5)

# Search Frame
frame_search = tk.Frame(root, pady=5)
frame_search.pack(pady=5, fill=tk.X)
set_frame_color(frame_search, 2)

tk.Label(frame_search, text="Search by Name or Roll").pack(side=tk.LEFT, padx=5)
entry_search = tk.Entry(frame_search)
entry_search.pack(side=tk.LEFT, padx=5)
entry_search.bind("<KeyRelease>", search_student)
btn_show_all = tk.Button(frame_search, text="Show All", command=refresh_tree)
btn_show_all.pack(side=tk.LEFT, padx=5)

# Treeview Frame
frame_tree = tk.Frame(root)
frame_tree.pack(expand=True, fill=tk.BOTH, pady=10)
set_frame_color(frame_tree, 3)

columns = ("Roll", "Name", "Age", "Grade")
tree = ttk.Treeview(frame_tree, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(expand=True, fill=tk.BOTH, pady=10)
tree.bind("<<TreeviewSelect>>", select_student)

# Delete button
btn_delete = tk.Button(root, text="Delete Selected", command=delete_student, state=tk.DISABLED)
btn_delete.pack(pady=5)

# Colorful bottom frame
frame_color = tk.Frame(root, height=80)
frame_color.pack(fill=tk.X, pady=5)
for i, color in enumerate(colors):
    sub_frame = tk.Frame(frame_color, bg=color, width=150, height=80)
    sub_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# Initialize tree
refresh_tree()
root.mainloop()
