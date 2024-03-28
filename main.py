import json
import string
import tkinter as tk
from tkinter import ttk
import random

def login(email_master, password_master):
    try:
        accounts = getacount()
        found = False
        for account in accounts:
            if account["email"] == email_master and account["password"] == password_master:
                found = True
                print(account["email"])  # Moved the print statement here
                break
        if found:
            print(found)
        else:
            print(found)
    except Exception as e:
        print(e)

def getacount():
    try:
        with open("acounts.json", "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return []

def run_settings():
    toggle_theme(check_theme())
    print("Settings loaded.")
    
def toggle_theme(toggle_name):
    # Toggle between themes
    match toggle_name:
        case "Dark" :
                # Dark mode
            style = ttk.Style()
            style.configure("TFrame", background="#35383f", bordercolor="white")
            style.configure("TLabelframe", background="#222222", bordercolor="white")
            style.configure("TLabel", foreground="#444444")
            style.configure("TEntry", background="#333333", foreground="#444444")
            style.configure("TButton", background="#333333", foreground="#444444")
            style.configure("TCheckbutton", background="#333333", foreground="#444444")
            frame1_inner.configure(background="#35383f", highlightbackground="white")
            frame1_inner2.configure(background="#35383f", highlightbackground="white")
            frame2_inner.configure(background="#35383f", highlightbackground="white")
            frame3_inner.configure(background="#35383f", highlightbackground="white")
            change_theme_json("Dark")
            
        case "Light" :
            # Light mode
            style = ttk.Style()
            style.configure("TFrame", background="white")
            style.configure("TLabelframe", background="white")
            style.configure("TLabel", foreground="black")
            style.configure("TEntry", background="white", foreground="black")
            style.configure("TButton", background="white", foreground="black")
            style.configure("TCheckbutton", background="white", foreground="black")
            frame1_inner2.configure(background="white")
            frame1_inner.configure(background="white")
            frame2_inner.configure(background="white")
            frame3_inner.configure(background="white")
            change_theme_json("Light")

def change_theme_json(change_theme):
    # Rewrite the settings.json file with the theme value changed
    toggle_button.configure(text=next_theme() + " mode")
    with open("settings.json", "r") as json_file:
        data = json.load(json_file)
    data[0] = "theme: " + change_theme
    with open("settings.json", "w") as json_file:
        json.dump(data, json_file)

def check_theme():
    try:
        # Read the settings JSON file
        with open("settings.json", "r") as json_file:
            settings_data = json.load(json_file)
        
        # Check if the "toggle_theme" variable exists
        if "theme: Dark" in settings_data:
            return "Dark"
        elif "theme: Light" in settings_data:
            return "Light"
    
    except FileNotFoundError:
        print("Settings file not found.")
        return False
    except json.decoder.JSONDecodeError:
        print("Error decoding JSON data.")
        return False

def next_theme():
    current_theme = check_theme()
    if current_theme == "Dark":
        return "Light"
    elif current_theme == "Light":
        return "Dark"
        
def load_passwords():
    try:
        with open("passwords.json", "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return []

def display_passwords():
    # Clear existing items in the Treeview widget
    for item in tree.get_children():
        tree.delete(item)
    
    passwords = load_passwords()
    for idx, password in enumerate(passwords, start=1):
        source = password["Source"]
        username = password["Username"]
        password_text = password["Password"]
        tree.insert("", "end", values=(idx, source, username, "*" * len(password_text)))
    

def paste_user():
    # Paste the username from clipboard into the entry field
    entry_username.delete(0, "end")
    entry_username.insert(0, root.clipboard_get())

def paste_password():
    # Paste the password from clipboard into the entry field
    entry_password.delete(0, "end")
    entry_password.insert(0, root.clipboard_get())

def on_button_click():
    username = entry_username.get()
    password = entry_password.get()
    source = entry_source.get()
    print("Source:", source)
    print("Username:", username)
    print("Password:", password)
    
    # Sample data
    new_data = {
        "Source": source,
        "Username": username,
        "Password": password
    }
    
    # Specify the file path
    file_path = "passwords.json"
    
    try:
        # Read existing data from the JSON file
        with open(file_path, "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []
    except json.decoder.JSONDecodeError:
        existing_data = []
    
    # Ensure existing data is a list
    if not isinstance(existing_data, list):
        existing_data = []
    
    # Append new data to the existing data
    existing_data.append(new_data)
    
    # Write data back to the JSON file
    with open(file_path, "w") as json_file:
        json.dump(existing_data, json_file)

    print("Data has been appended to", file_path)

def GeneratePassword(length=14):
    password = string.ascii_letters + string.digits + string.punctuation
    GeneratePasswordText.configure(text="Password: " + ''.join(random.choice(password) for i in range(length)))
    return ''.join(random.choice(password) for i in range(length))

def copy_generated_password():
    label_text = GeneratePasswordText["text"][10:20]
    root.clipboard_clear()
    root.clipboard_append(label_text)

def button_search():
    username_term = username_search.get()
    source_term = source_search.get()
    if (username_term != ""):
        tree.delete(*tree.get_children())
        passwords = load_passwords()
        for index,password in enumerate(passwords, start=1):
            if username_term in password["Username"]:
                tree.insert("", "end", values=(index, password["Source"], password["Username"],"*" *  len(password["Password"])))
    elif (source_term != ""):
        tree.delete(*tree.get_children())
        passwords = load_passwords()
        for index,password in enumerate(passwords, start=1):
            if source_term in password["Source"]:
                tree.insert("", "end", values=(index, password["Source"], password["Username"],"*" * len(password["Password"])))

    print(username_term)
    print(source_term)
    print("end")

def check_password(password):
    characteristics = []
    
    if any(char.islower() for char in password):
        characteristics.append('lowercase')
    if any(char.isupper() for char in password):
        characteristics.append('uppercase')
    if any(char.isdigit() for char in password):
        characteristics.append('numbers')
    if any(char in string.punctuation for char in password):
        characteristics.append('special characters')

    message = "containing {} characters".format(len(password))
    if characteristics:
        message += ", " + ", ".join(characteristics)
    
    return message

def update_bar(password):
    total = 0
    islower = 0
    isupper = 0
    isdigit = 0
    isspecial = 0
    print(total)
    if any(char.islower() for char in password):
        islower += 1
    else:
        if (islower > 0):
            islower -= 1
    if any(char.isupper() for char in password):
        isupper += 1
    else:
        if (isupper > 0):
            isupper -= 1
    if any(char.isdigit() for char in password):
        isdigit += 1
    else:
        if (isdigit > 0):
            isdigit -= 1
    if any(char in string.punctuation for char in password):
        isspecial += 1
    else:
        if (isspecial > 0):
            isspecial -= 1
    total = islower + isupper + isdigit + isspecial
    bar_fill_size = total * 10  
    bar_fill.set(int(bar_fill_size) * "|")

def save_password(password):
    with open("passwords.json", "r") as json_file:
        data = json.load(json_file)
    data.append(password)
    with open("passwords.json", "w") as json_file:
        json.dump(data, json_file)

def change_password(source,password,username,new_password,new_username,new_source):
    i = 0
    print("Changing password...")
    with open("passwords.json", "r") as json_file:
        data = json.load(json_file)
    for item in data:
        print(source, username, password, new_password, new_username, new_source, i)
        i = i+1
        if item["Source"] == source and item["Username"] == username and item["Password"] == password:
            print("found")
            item["Source"] = new_source
            item["Password"] = new_password
            item["Username"] = new_username
            print("done")
            break
    with open("passwords.json", "w") as json_file:
        json.dump(data, json_file)

def save_changes(edit_window, source, username, password, new_password, new_username, new_source):
    # Update the password data
    change_password(source, password, username, new_password, new_username, new_source)

    # Refresh the tree to reflect changes
    display_passwords()
 
    # Close the edit window
    edit_window.destroy()

def edit_button_click():
    # Get the selected item(s) from the tree
    selected_items = tree.selection()
    if not selected_items:
        print("Please select a password to edit.")
        return

    # We'll assume only one item can be selected for editing
    selected_item = selected_items[0]

    # Get the values of the selected item
    values = tree.item(selected_item, "values")
    if not values:
        print("Invalid selection.")
        return

    # Extract relevant data (source, username, password)
    source = values[1]
    username = values[2]
    password = values[3]

    # Create a new toplevel window for editing
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Password")

    # Create and arrange widgets for editing
    label_edit_source = tk.Label(edit_window, text="Source:")
    label_edit_source.grid(row=0, column=0, padx=10, pady=5)
    entry_edit_source = tk.Entry(edit_window)
    entry_edit_source.insert(0, source)
    entry_edit_source.grid(row=0, column=1, padx=10, pady=5)

    label_edit_username = tk.Label(edit_window, text="Username:")
    label_edit_username.grid(row=1, column=0, padx=10, pady=5)
    entry_edit_username = tk.Entry(edit_window)
    entry_edit_username.insert(0, username)
    entry_edit_username.grid(row=1, column=1, padx=10, pady=5)

    label_edit_password = tk.Label(edit_window, text="Password:")
    label_edit_password.grid(row=2, column=0, padx=10, pady=5)
    entry_edit_password = tk.Entry(edit_window)
    entry_edit_password.insert(0, password)
    entry_edit_password.grid(row=2, column=1, padx=10, pady=5)

    # Button to save changes
    save_button = tk.Button(edit_window, text="Save Changes", command=lambda: save_changes(edit_window, source, username, password, entry_edit_password.get(), entry_edit_username.get(), entry_edit_source.get()))
    save_button.grid(row=3, columnspan=2, padx=10, pady=10)



# Create the main application window---------------------------------------------------------------------------------------------------------------------------------------------------------------
root = tk.Tk()
root.title("Password Manager")


# Change the icon of the application
root.iconbitmap("secret.ico")  

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill=tk.BOTH)


# First tab----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text='Create Password')

# Create and configure a frame to organize widgets in the first tab
frame1_inner = tk.Frame(frame1)
frame1_inner.pack(padx=500, pady=200)

# Create a label widget in the first tab
frame1_inner2 = tk.Frame(frame1_inner)
frame1_inner2.pack(side="right")

label_username = tk.Label(frame1_inner, text="Username:", font=("Arial", 10))
label_username.pack(pady=10)

entry_username = tk.Entry(frame1_inner, font=("Arial", 10))
entry_username.pack(pady=10)

label_password = tk.Label(frame1_inner, text="Password:", font=("Arial", 10))
label_password.pack(pady=0)

entry_password = tk.Entry(frame1_inner, font=("Arial", 10), show="*")  
entry_password.pack(pady=10)

label_source = tk.Label(frame1_inner, text="Source:", font=("Arial", 10))
label_source.pack(pady=10)

entry_source = tk.Entry(frame1_inner, font=("Arial", 10))
entry_source.pack(pady=10)

button = tk.Button(frame1_inner, text="Create Password!", font=("Arial", 14), command=on_button_click)
button.pack(pady=10)

button = tk.Button(frame1_inner2, text="Generate Password!", font=("Arial", 14), command=GeneratePassword)
button.pack(pady=10)

# Generate Password
GeneratePasswordText = tk.Label(frame1_inner2, text="Generate Password: x", font=("Arial", 14))
GeneratePasswordText.pack(pady=10)

button = tk.Button(frame1_inner2, text="Copy Generated Password", font=("Arial", 14), command=copy_generated_password)
button.pack(pady=10)

# Second tab------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
frame2 = ttk.Frame(notebook)
notebook.add(frame2, text='Load passwords')

# Create and configure a frame to organize widgets in the second tab
frame2_inner = tk.Frame(frame2)
frame2_inner.pack(padx=20, pady=20)

label_U = tk.Label(frame2_inner, text="Username:", font=("Arial", 10))
label_U.pack(side="left", padx=10, pady=10)

username_search = tk.Entry(frame2_inner, font=("Arial", 10))
username_search.pack(side="left", padx=10, pady=10)

label_S = tk.Label(frame2_inner, text="Scource:", font=("Arial", 10))
label_S.pack(side="left", padx=10, pady=10)

source_search = tk.Entry(frame2_inner, font=("Arial", 10))
source_search.pack(side="left", padx=10, pady=10)
source_search.pack(pady=10)

search_button = tk.Button(frame2_inner, text="Search", font=("Arial", 10), command=button_search)
search_button.pack(side="left", padx=10, pady=10)

# Create a Treeview widget to display passwords
tree = ttk.Treeview(frame2, columns=("Index", "Source", "Username", "Password"), show="headings")
tree.heading("Index", text="Index")
tree.heading("Source", text="Source")
tree.heading("Username", text="Username")
tree.heading("Password", text="Password")
tree.pack(fill=tk.BOTH, expand=True)

# Button to load and display passwords
load_button = tk.Button(frame2, text="Load Passwords", command=display_passwords)
load_button.pack()

# Button to edit the password
edit_button = tk.Button(frame2, text="Edit Password", command=edit_button_click)
edit_button.pack(pady=5)


# Bind keys "q" and "w" to paste_user() and paste_password() functions
root.bind("q", paste_user)
root.bind("w", paste_password)

# third tab----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
frame3 = ttk.Frame(notebook)
notebook.add(frame3, text='Settings')

label3 = tk.Label(frame3, text=check_theme() + " mode", font=("Arial", 18))
label3.pack(pady=10)
# Create and configure a frame to organize widgets in the second tab
frame3_inner = tk.Frame(frame3)
frame3_inner.pack(padx=20, pady=20)

# Create a Checkbutton widget for theme switching in the third tab
toggle_button = tk.Button(frame3_inner, text=next_theme() + " mode", command= lambda : toggle_theme(next_theme()))
toggle_button.pack(pady=10)

# fourth tab----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
frame4 = ttk.Frame(notebook)
notebook.add(frame4, text='Login')

frame4_inner = tk.Frame(frame4)
frame4_inner.pack(padx=80, pady=80)

label4_2 = tk.Label(frame4_inner, text="Email:", font=("Arial", 10))
label4_2.pack(side="left",pady=10)

entry3_1 = tk.Entry(frame4_inner, font=("Arial", 10))
entry3_1.pack(side="left",pady=10)

label4_2 = tk.Label(frame4_inner, text="Password:", font=("Arial", 10))
label4_2.pack(side="left",pady=10)

entry3_2 = tk.Entry(frame4_inner, font=("Arial", 10))
entry3_2.pack(side="right",pady=10)

button_login = tk.Button(frame4_inner, text="Login", font=("Arial", 10), command= lambda : login(entry3_1.get(), entry3_2.get()))
button_login.pack(side="bottom",pady=50)

# fifth tab----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
frame5 = ttk.Frame(notebook)
notebook.add(frame5, text='password Strenght')

frame5_inner = tk.Frame(frame5)
frame5_inner.pack(padx=80, pady=80)

label5_1 = tk.Label(frame5_inner, text="password:", font=("Arial", 10))
label5_1.pack(pady=10)

entry5_1 = tk.Entry(frame5_inner, font=("Arial", 10))
entry5_1.pack(pady=10)

label5_2 = tk.Label(frame5_inner, text="characters containing:", font=("Arial", 10))
label5_2.pack(padx=10,pady=10)

frame5_bar = tk.Frame(frame5_inner, width=200, height=20, background="grey")
frame5_bar.pack(pady=20)

bar_fill = tk.StringVar()
bar_fill.set("")

entry5_1.bind("<KeyRelease>", lambda event: (label5_2.config(text="characters containing: " + check_password(entry5_1.get())), update_bar(entry5_1.get())))


bar_label = tk.Label(frame5_bar, textvariable=bar_fill, background="green")
bar_label.pack(side="left")
bar_label.config(borderwidth=1, relief="sunken") # can you put a box around the label

# To run last and one time-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

run_settings()
display_passwords()


# Run the application
root.mainloop()

