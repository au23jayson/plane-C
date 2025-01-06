import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.simpledialog import askstring
from time import strftime
from tkcalendar import Calendar, DateEntry
from datetime import datetime, timedelta
from PIL import Image, ImageTk


def digital_clock():
    current_time = strftime('%I:%M:%S %p')  
    time_var.set(current_time)
    root.after(1000, digital_clock)


def date():
    date_string = strftime('%B %d, %Y')  
    date_label.config(text=date_string)


def add_task():
    task = task_entry.get()
    start_time = start_time_entry.get()
    end_time = end_time_entry.get()
    task_date = date_entry.get()  

    if task and start_time and end_time and task_date:
        task_list.insert(tk.END, f"{task_date} - {task} ({start_time} - {end_time})")
        task_entry.delete(0, tk.END)
        start_time_entry.delete(0, tk.END)
        end_time_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)  
        
        
        selected_date = task_date
        selected_dates.add(selected_date)
        cal.calevent_create(selected_date, "Schedule", task, background="green")
        date_dropdown['menu'].delete(0, "end")
        for date in selected_dates:
            date_dropdown['menu'].add_command(label=date, command=tk._setit(date_var, date))
    else:
        messagebox.showwarning("Warning", "Task, Start Time, End Time, and Date cannot be empty!")


def remove_task():
    selected_task_index = task_list.curselection()
    if selected_task_index:
        selected_task = task_list.get(selected_task_index)
        confirm = askstring("Task Confirmation", f"Is the task '{selected_task}' finished? (yes/no)")
        if confirm and confirm.lower() == "yes":
            task_list.delete(selected_task_index)
            messagebox.showinfo("Congratulations", "Good job on finishing a task!")
    else:
        messagebox.showwarning("Warning", "Select a task to remove!")


def choose_date():
    selected_date = date_var.get()
    cal.set_date(selected_date)


def validate_date():
    try:
        date_str = date_entry.get()
        date_obj = datetime.strptime(date_str, "%m/%d/%Y")
        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30)
        
        if thirty_days_ago <= date_obj <= today:
            return True
        else:
            messagebox.showwarning("Warning", "Date must be within the last 30 days and today.")
            return False
    except ValueError:
        messagebox.showwarning("Warning", "Invalid date format. Use MM/DD/YYYY.")
        return False


def change_background():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])

    if file_path:
        root.background_image = Image.open(file_path)
        root.background_photo = ImageTk.PhotoImage(root.background_image)
        bg_label.config(image=root.background_photo)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.image = root.background_photo  


root = tk.Tk()
root.title("Digital Clock with Date, To-Do List, and Calendar")


window_width = 900
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")


date_label = tk.Label(root, font=('system', 20, 'bold'))
date_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)


date()


bg_label = tk.Label(root)
bg_label.place(relwidth=1, relheight=1)  


task_label = tk.Label(root, text="Task:", font=('system', 14))
task_label.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
task_entry = tk.Entry(root, font=('system', 14))
task_entry.grid(row=1, column=1, padx=10, pady=5, sticky="e")


start_time_label = tk.Label(root, text="Start Time:", font=('system', 14))
start_time_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
start_time_entry = tk.Entry(root, font=('system', 14), width=8)
start_time_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

end_time_label = tk.Label(root, text="End Time:", font=('system', 14))
end_time_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
end_time_entry = tk.Entry(root, font=('system', 14), width=8)
end_time_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")


date_label = tk.Label(root, text="Input Date:", font=('system', 14))
date_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
date_entry = DateEntry(root, font=('system', 14), width=10, date_pattern='mm/dd/yyyy', validate="focusout", validatecommand=validate_date)
date_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")


add_button = tk.Button(root, text="Add Task", font=('system', 14), command=add_task)
add_button.grid(row=5, column=0, padx=10, pady=5, sticky="w")

remove_button = tk.Button(root, text="Remove Task", font=('system', 14), command=remove_task)
remove_button.grid(row=5, column=1, padx=10, pady=5, sticky="e")


task_frame = tk.Frame(root)
task_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

task_list = tk.Listbox(task_frame, font=('system', 14), selectmode=tk.SINGLE)
task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

task_scrollbar = tk.Scrollbar(task_frame, orient=tk.VERTICAL)
task_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_list.config(yscrollcommand=task_scrollbar.set)
task_scrollbar.config(command=task_list.yview)


date_var = tk.StringVar()
date_var.set("")  
date_dropdown = tk.OptionMenu(root, date_var, "")
date_dropdown.grid(row=5, column=2, padx=10, pady=5, sticky="e")
date_label = tk.Label(root, text="Choose Date:", font=('system', 14))
date_label.grid(row=5, column=3, padx=10, pady=5, sticky="w")


cal = Calendar(root, font=('system', 14), date_pattern='mm/dd/yyyy')
cal.grid(row=6, column=3, rowspan=1, padx=10, pady=10, sticky="nsew")


selected_dates = set()


bg_button = tk.Button(root, text="Change Background", font=('system', 11), command=change_background)
bg_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="w")


time_var = tk.StringVar()
label_time = tk.Label(root, font=('system', 30, 'bold'), textvariable=time_var)
label_time.grid(row=1, column=3, columnspan=4, padx=10, pady=10, sticky="nsew")


digital_clock()


root.mainloop()
  