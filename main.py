import tkinter
import customtkinter
import secrets
import string
from cryptography.fernet import Fernet
import os

# Key management
KEY_FILE = "key.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

key = load_key()
cipher_suite = Fernet(key)

def create_password():
    clear_window()

    def generate():
        inputted_password_length = int(password_length_var.get())
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for i in range(inputted_password_length))
        password_display_var.set(password)
        save_password(password)

    password_length_var = tkinter.StringVar()
    password_display_var = tkinter.StringVar()

    length_label = customtkinter.CTkLabel(program, text="Enter password length:")
    length_label.pack(padx=10, pady=10)

    password_length_entry = customtkinter.CTkEntry(program, width=200, height=30, textvariable=password_length_var)
    password_length_entry.pack(padx=10, pady=10)

    generate_button = customtkinter.CTkButton(program, text="Generate", command=generate, width=200, height=40)
    generate_button.pack(padx=10, pady=10)

    password_label = customtkinter.CTkLabel(program, textvariable=password_display_var)
    password_label.pack(padx=10, pady=10)

    back_button = customtkinter.CTkButton(program, text="Back", command=main_menu, width=200, height=40)
    back_button.pack(padx=10, pady=10)

def save_password(password):
    encrypted_password = cipher_suite.encrypt(password.encode())
    with open("passwords.txt", "a") as file:
        file.write(encrypted_password.decode() + "\n")
    print("Password Saved to passwords.txt")

def see_password():
    clear_window()

    decrypted_passwords_var = tkinter.StringVar()

    try:
        with open("passwords.txt", "r") as file:
            content = file.readlines()
            decrypted_passwords = []
            for line in content:
                line = line.strip()
                if line:  # skip empty lines
                    try:
                        decrypted_password = cipher_suite.decrypt(line.encode()).decode()
                        decrypted_passwords.append(decrypted_password)
                    except Exception as e:
                        print(f"Skipping line due to decryption error: {line} - Error: {e}")
            if decrypted_passwords:
                passwords_text = "\n".join(decrypted_passwords)
                decrypted_passwords_var.set(passwords_text)
            else:
                decrypted_passwords_var.set("No passwords found.")
    except FileNotFoundError:
        decrypted_passwords_var.set("No passwords saved yet.")
    except Exception as e:
        decrypted_passwords_var.set(f"An error occurred: {e}")

    decrypted_passwords_label = customtkinter.CTkLabel(program, textvariable=decrypted_passwords_var)
    decrypted_passwords_label.pack(padx=10, pady=10)

    back_button = customtkinter.CTkButton(program, text="Back", command=main_menu, width=200, height=40)
    back_button.pack(padx=10, pady=10)

def clear_window():
    for widget in program.winfo_children():
        widget.pack_forget()

def main_menu():
    clear_window()

    title = customtkinter.CTkLabel(program, text="Welcome to the program")
    title.pack(padx=10, pady=(80, 10))

    generate_password_choice = customtkinter.CTkButton(program, text="Generate a secure password", command=create_password, width=200, height=40)
    generate_password_choice.pack(padx=10, pady=10)

    see_saved_passwords_choice = customtkinter.CTkButton(program, text="See saved passwords", command=see_password, width=200, height=40)
    see_saved_passwords_choice.pack(padx=10, pady=10)

# Configuration
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# the program window
program = customtkinter.CTk()
program.geometry("720x480")
program.title("Password Manager")

# Display the main menu
main_menu()

# main loop for the GUI
program.mainloop()
