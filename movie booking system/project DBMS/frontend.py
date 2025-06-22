import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import backend

root = tk.Tk()
root.title("Online Movie Ticket Booking System")
root.geometry("1000x600")
root.configure(bg="black")

# Entry variables
movie_vars = {
    "movie_id": tk.StringVar(),
    "name": tk.StringVar(),
    "release_date": tk.StringVar(),
    "director": tk.StringVar(),
    "cast": tk.StringVar(),
    "budget": tk.StringVar(),
    "duration": tk.StringVar(),
    "rating": tk.StringVar()
}

selected_movie_id = None  # Global variable

# Labels and Entry Widgets
def create_label_entry(frame, text, var, row):
    tk.Label(frame, text=text, font=('Arial', 12, 'bold'), fg='orange', bg='black').grid(row=row, column=0, sticky='w')
    tk.Entry(frame, textvariable=var, width=30).grid(row=row, column=1)

left_frame = tk.LabelFrame(root, text="Movie Info", font=('Arial', 16, 'bold'), fg='white', bg='black')
left_frame.place(x=20, y=20, width=480, height=350)

for idx, (key, var) in enumerate(movie_vars.items()):
    create_label_entry(left_frame, key.replace("_", " ").title() + ":", var, idx)

# Movie List
movie_list = tk.Listbox(root, height=15, width=80)
movie_list.place(x=530, y=50)
scroll = tk.Scrollbar(root)
scroll.place(x=990, y=50, height=245)
movie_list.config(yscrollcommand=scroll.set)
scroll.config(command=movie_list.yview)

def get_selected_row(event):
    global selected_movie_id
    if not movie_list.curselection():
        return
    index = movie_list.curselection()[0]
    selected = movie_list.get(index)
    selected_movie_id = int(selected.split()[0])
    data = backend.ViewMovieData()
    for row in data:
        if row[0] == selected_movie_id:
            keys = list(movie_vars.keys())
            for i in range(len(keys)):
                movie_vars[keys[i]].set(row[i+1])
            break

movie_list.bind("<<ListboxSelect>>", get_selected_row)

# Command Functions
def clear_fields():
    for var in movie_vars.values():
        var.set("")
    movie_list.selection_clear(0, tk.END)

def add_movie():
    backend.AddMovieRec(*[var.get() for var in movie_vars.values()])
    messagebox.showinfo("Success", "Movie added successfully")
    display_movies()
    clear_fields()

def display_movies():
    movie_list.delete(0, tk.END)
    for row in backend.ViewMovieData():
        movie_list.insert(tk.END, f"{row[0]} {row[2]} {row[3]} {{{row[4]}}} {{{row[5]}}}")

def search_movies():
    results = backend.SearchMovieData(*[var.get() for var in movie_vars.values()])
    movie_list.delete(0, tk.END)
    for row in results:
        movie_list.insert(tk.END, f"{row[0]} {row[2]} {row[3]} {{{row[4]}}} {{{row[5]}}}")

def delete_movie():
    global selected_movie_id
    if selected_movie_id:
        backend.DeleteMovieRec(selected_movie_id)
        messagebox.showinfo("Deleted", "Movie deleted successfully")
        display_movies()
        clear_fields()
        selected_movie_id = None
    else:
        messagebox.showwarning("Error", "Select a movie to delete")

def update_movie():
    global selected_movie_id
    if selected_movie_id:
        backend.UpdateMovieRec(selected_movie_id, *[var.get() for var in movie_vars.values()])
        messagebox.showinfo("Updated", "Movie updated successfully")
        display_movies()
    else:
        messagebox.showwarning("Error", "Select a movie to update")

def book_ticket():
    global selected_movie_id
    if not selected_movie_id:
        messagebox.showwarning("Error", "Select a movie to book tickets")
        return

    # Get movie name
    movie_data = backend.ViewMovieData()
    movie_name = None
    for row in movie_data:
        if row[0] == selected_movie_id:
            movie_name = row[2]
            break

    if not movie_name:
        messagebox.showwarning("Error", "Movie not found")
        return

    def submit_booking():
        name = entry_name.get()
        tickets = entry_tickets.get()
        if not name or not tickets.isdigit():
            messagebox.showerror("Error", "Enter valid details")
            return
        backend.AddBooking(movie_name, int(tickets), name)
        messagebox.showinfo("Booked", "Tickets booked successfully")
        top.destroy()

    top = tk.Toplevel(root)
    top.title("Book Tickets")
    top.geometry("300x200")
    tk.Label(top, text="Customer Name").pack(pady=5)
    entry_name = tk.Entry(top)
    entry_name.pack(pady=5)
    tk.Label(top, text="Number of Tickets").pack(pady=5)
    entry_tickets = tk.Entry(top)
    entry_tickets.pack(pady=5)
    tk.Button(top, text="Submit", command=submit_booking).pack(pady=10)

# Buttons
buttons = [
    ("Add New", add_movie),
    ("Display", display_movies),
    ("Clear", clear_fields),
    ("Search", search_movies),
    ("Delete", delete_movie),
    ("Update", update_movie),
    ("Book Ticket", book_ticket)
]

for i, (text, cmd) in enumerate(buttons):
    tk.Button(root, text=text, width=15, bg="orange", font=('Arial', 12, 'bold'), command=cmd)\
        .place(x=20 + i*135, y=400)

root.mainloop()
