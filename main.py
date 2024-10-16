import os
from tkinter import *
import random as rd
from tkinter import messagebox
import json

SMALL_CHARACTERS = [chr(i) for i in range(97, 123)]
CAPITAL_LETTERS = [chr(i) for i in range(65, 91)]
SPECIAL_CHARACTERS = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+', '[', ']', '{', '}', ';', ':',
                      ',', '.', '/', '<', '>', '?']
NUMBERS = [str(i) for i in range(0, 10)]


# ---------------------------- SEARCH FUNTIONALITY ------------------------------- #
def search():
    try:
        with open('Login_credentials.json','r') as f:
            if os.stat('Login_credentials.json').st_size == 0:
                data = {}
            else:
                data = json.load(f)
    except FileNotFoundError:
        messagebox.showwarning('ERR!!','File not found')
    else:
        name = website_name_in.get()
        if name in data:
            credentials_retrieved=data[name]
            username_email=credentials_retrieved['email']
            password = credentials_retrieved['password']
            messagebox.showinfo('login credentials retrieved!}',f'The credentials of {name}\nEmail/Username:{username_email}\nPassword:{password}')
        else:
            messagebox.showwarning('Sorry!!','No details found')
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pass():
    pass_list = SMALL_CHARACTERS + CAPITAL_LETTERS + SPECIAL_CHARACTERS
    rd.shuffle(pass_list)
    pass_to_append = rd.sample(pass_list, 11) + rd.sample(NUMBERS, k=3)
    password = ''.join(rd.sample(pass_to_append, 14))
    password_in.delete(0, END)
    password_in.insert(0, password)
    win.clipboard_clear()
    win.clipboard_append(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_credentials():
    global number_of_credentials
    website_name = website_name_in.get()
    email_or_username = email_or_username_txt_in.get()
    password = password_in.get()
    credential_data = {
        website_name: {
            'email': email_or_username,
            'password': password
        }
    }
    if not (website_name and email_or_username and password):
        messagebox.showwarning("Input Required", "To add the Credentials \nPlease fill all the field.")
    else:
        messagebox.askyesno(title=website_name,
                            message=f'Website Name: {website_name}\nUsername/Email: {email_or_username}\nPassword: {password}\nIs it ok to save?')
        try:
            with open('Login_credentials.json', 'r') as f:
                if os.stat('Login_credentials.json').st_size == 0:
                    data = {}
                else:
                    data = json.load(f)
        except FileNotFoundError:
            with open('Login_credentials.json', 'w') as f:
                json.dump(credential_data, f, indent=4)
        else:
            print(data)
            data.update(credential_data)
            print(data)
            with open('Login_credentials.json', 'w') as f:
                json.dump(data, f, indent=4)
        finally:
            website_name_in.delete(0, END)
            email_or_username_txt_in.delete(0, END)
            password_in.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
win = Tk()
win.geometry('490x360')
win.config(pady=30, padx=30)
win.title('Password Manager')
win.config(bg='white')  # Set background to white

# Create a canvas for the image
canva = Canvas(win, width=200, height=190, bg='white', highlightthickness=0)  # Remove border highlight
image_path = PhotoImage(file='logo.png')  # Ensure this path is correct
canva.create_image(100, 95, image=image_path)
canva.grid(column=1, row=0)

# Label for website name
web_name_txt = Label(win, text='Website Name:', font=('Helvetica', 9), bg='white', fg='black')
web_name_txt.grid(column=0, row=1)

# Entry for website name
website_name_in = Entry(win, width=52, bg='lightgray')  # Optional light background for entry
website_name_in.grid(column=1, row=1, columnspan=2)

# Label for email/username
email_or_username_txt = Label(win, text='Email/Username:', font=('Helvetica', 9), bg='white', fg='black')
email_or_username_txt.grid(row=2, column=0)

# Entry for email/username
email_or_username_txt_in = Entry(win, width=52, bg='lightgray')  # Optional light background for entry
# email_or_username_txt_in.insert('ENTER YOUR EMAIL IF YOU DON'T WANT TO ENTER IT EVERY SINGLE TIME')
email_or_username_txt_in.grid(column=1, row=2, columnspan=2)

# Corrected label for password
password_txt = Label(win, text='Password:', font=('Helvetica', 9), bg='white', fg='black')
password_txt.grid(row=3, column=0)

# Entry for password
password_in = Entry(win, width=34, bg='lightgray')  # Optional light background for entry
password_in.grid(column=1, row=3)

# Button to generate password
generate_button = Button(win, text='Generate Password', width=14, command=generate_pass, bg='white', fg='black')
generate_button.grid(row=3, column=2)

# Add the button to save the details on the local system
add_button = Button(win, text='Add', width=44, command=save_credentials, bg='white', fg='black')
add_button.grid(row=4, column=1, columnspan=2)

# search button
search_button = Button(win, text='search', width=14, command=search, bg='white', fg='black')
search_button.grid(row=1, column=2)

# Start the Tkinter event loop
win.mainloop()
