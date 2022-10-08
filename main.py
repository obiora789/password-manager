from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

padding = 50
canvas_measurement = 200
FONT_NAME = "Arial"


# -----------------------------SEARCH FOR LOGIN DETAILS---------------------------- #
def search():
    """This method performs a search using the website as a key on entries and displays the login details
    for the website stored in its database. It also copies the password to the clipboard"""
    found = False
    website = website_entry.get().title()
    try:
        with open("data.json", mode="r") as open_file:
            search_data = json.load(open_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops!", message="Data file does not exist.")
    else:
        for key, value in search_data.items():
            if website == key:
                email_value = value["email"]
                password_value = value["password"]
                pyperclip.copy(password_value)
                messagebox.showinfo(title="NOTICE", message=f"Username: {email_value}\n "
                                                            f"Password: {password_value}")
                found = True
                break
        if len(website) == 0:
            messagebox.showinfo(title="Oops!!", message="Please, do not leave the website field empty.")
        elif not found:
            messagebox.showinfo(title="NOTICE", message=f"{website} record does not exist!")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """This method generates random passwords and is called once the
    'Generate password' button is clicked."""
    gen_password.config(command="")
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
               'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
               'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
               'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_list += [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_list += [random.choice(numbers) for _ in range(random.randint(2, 4))]
    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def write_data(data):
    """Method to write data"""
    with open("data.json", mode="w") as new_file:
        json.dump(data, new_file, indent=4)


def check_new_data():
    """This method creates, reads, checks and updates valid data """
    extension = True
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        },
    }
    try:
        with open("data.json", mode="r") as read_file:
            read_data = json.load(read_file)
    except FileNotFoundError:
        write_data(new_data)
        messagebox.showinfo(title="NOTICE!", message="Your details have been saved.")
    else:
        for key, value in read_data.items():
            if website == key and email == value["email"]:
                messagebox.askyesno(title=website, message="You have an existing record. "
                                                           "Do you want to overwrite "
                                                           "your password?")
                extension = False
        if extension:
            read_data.update(new_data)
            write_data(read_data)
            messagebox.showinfo(title="NOTICE!", message="Your details have been saved.")


def save():
    """This method saves valid entries as a record in data.json"""
    website_value = website_entry.get().title()
    password_value = password_entry.get()
    gen_password.config(command=generate_password)
    if len(website_value) == 0 or len(password_value) == 0:
        messagebox.showinfo(title="Oops!!", message="Please don't leave any field empty.")
    else:
        check_new_data()
        website_entry.delete(0, END)
        email_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=padding, pady=padding)
# Canvas
canvas = Canvas(width=canvas_measurement, height=canvas_measurement, highlightthickness=0)
padlock_img = PhotoImage(file="logo.png")
canvas.create_image(canvas_measurement / 2, canvas_measurement / 2, image=padlock_img)
canvas.grid(row=0, column=0, columnspan=3)
# Website Label
website_label = Label(text="Website:", font=(FONT_NAME, 13, "normal"))
website_label.grid(row=1, column=0)
website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(row=1, column=1)
# Search Button
search_button = Button(text="Search", font=(FONT_NAME, 13, "normal"), width=11, command=search)
search_button.grid(row=1, column=2)
# Email Entry
email_label = Label(text="Email/Username:", font=(FONT_NAME, 13, "normal"))
email_label.grid(row=2, column=0)
email_entry = Entry(width=35)
email_entry.insert(0, "obioracelestine@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2)
# Password Entry
password_label = Label(text="Password:", font=(FONT_NAME, 13, "normal"))
password_label.grid(row=3, column=0)
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)
# Generate Password Button
gen_password = Button(text="Generate Password", font=(FONT_NAME, 13, "normal"), width=11)
gen_password.config(command=generate_password)
gen_password.grid(row=3, column=2)
# Add Button
add_button = Button(text="Add", font=(FONT_NAME, 13, "normal"), width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, pady=10)

window.mainloop()
