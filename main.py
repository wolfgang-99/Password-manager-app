from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

FONT_NAME = ("Courier", 10)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letter = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_char = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letter + password_symbols + password_char
    random.shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- search web info -----------------------------#

def search():
    web_info = web_input.get().upper()
    try:
        with open("data.json", mode="r") as info_file:
            data = json.load(info_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Erro", message="No Data File Found")
    else:
        if web_info in data:
            Email = data[web_info]["Email"]
            password = data[web_info]["Password"]
            messagebox.showinfo(title=f"{web_info}", message=f"Email:{Email}\n Password:{password}")
        else:
            messagebox.showinfo(title="erro", message=f"No details for {web_info} exist.")

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_details():
    web_data = web_input.get().upper()
    username_data = username_input.get()
    password_data = password_input.get()
    new_data = {
        web_data: {
            "Email": username_data,
            "Password": password_data,
        }
    }

    if len(web_data) == 0 or len(password_data) == 0:
        messagebox.showinfo(title="Oops", message="Please don't have any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=web_data, message=f"this are the details entered: "
                                                               f"\nEmail or Username: {username_data} "
                                                               f"\nPassword: {password_data} \nis it ok to save")

        if is_ok:
            try:
                with open(file="data.json", mode="r") as file:
                    # read old data
                    data = json.load(file)

            except FileNotFoundError:
                with open(file="data.json", mode="w") as file:
                    # open a file if an error of file not found occour and write into the file
                    json.dump(new_data, file, indent=4)

            else:
                # updating old data with new data
                data.update(new_data)

                with open(file="data.json", mode="w") as file:
                    # saving updated data
                    json.dump(data, file, indent=4)
            finally:
                web_input.delete(0, END)
                password_input.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("password manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
image_logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image_logo)
canvas.grid(row=0, column=1)

web_lable = Label(text="Website:", font=FONT_NAME)
web_lable.grid(row=1, column=0)

web_input = Entry(width=21)
web_input.focus()
web_input.grid(row=1, column=1)

username_lable = Label(text="Email/username:", font=FONT_NAME)
username_lable.grid(row=2, column=0)

username_input = Entry(width=35)
username_input.insert(0, "wolf@email.com")
username_input.grid(row=2, column=1, columnspan=2)

password_lable = Label(text="password:", font=FONT_NAME)
password_lable.grid(row=3, column=0)

password_input = Entry(width=21)
password_input.grid(row=3, column=1)

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=36, command=save_details)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text=" Search ", width=13, command=search)
search_button.grid(row=1, column=2)

window.mainloop()
