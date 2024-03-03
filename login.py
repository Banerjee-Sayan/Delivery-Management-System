import tkinter as tk
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
from io import BytesIO
import requests
import userbackend
from user import App

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.connection = userbackend.connect_to_database()
        self.user_backend = userbackend.UserBackend(self.connection)
        self.root.title("Login Page")
        self.root.geometry("400x200")

        # Set the minimum size and make the window non-resizable
        self.root.minsize(400, 200)
        self.root.resizable(False, False)

        # Create a frame for better organization
        frame = ttk.Frame(root, padding=(20, 20, 20, 20))  # Add padding to the frame
        frame.pack(expand=True, fill="both")

        # Create labels and entry widgets for User ID and Password
        user_id_label = ttk.Label(frame, text="User ID:")
        user_id_label.grid(row=0, column=0, pady=10, sticky="w")

        self.user_id_entry = ttk.Entry(frame, width=30)
        self.user_id_entry.grid(row=0, column=1, pady=10, sticky="ew")

        password_label = ttk.Label(frame, text="Password:")
        password_label.grid(row=1, column=0, pady=10, sticky="w")

        self.password_entry = ttk.Entry(frame, show="*", width=30)  # Passwords are shown as asterisks
        self.password_entry.grid(row=1, column=1, pady=10, sticky="ew")

        # Create a login button
        login_button = ttk.Button(frame, text="Login", command=self.login)
        login_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        registration_button = ttk.Button(frame, text="Register", command=self.open_registration_page)
        registration_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")



        

        # Center the frame on the screen
        frame.columnconfigure(0, weight=1)  # Make the first column expandable
        frame.columnconfigure(1, weight=1)  # Make the second column expandable
        frame.rowconfigure(2, weight=1)  # Make the third row expandable

        # Center the frame on the screen
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        self.center_window()

    def center_window(self):
        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width - 400) // 2
        y_coordinate = (screen_height - 200) // 2
        self.root.geometry(f"400x200+{x_coordinate}+{y_coordinate}")

    def login(self):
        # Get the entered User ID and Password
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()

        # Authenticate user
        if self.user_backend.authenticate_user(user_id, password):
            messagebox.showinfo("Login Successful", "Login successful!")
            # Open the user interface
            self.open_user_interface()
        else:
            messagebox.showerror("Login Failed", "Login failed. Invalid credentials.")
    
    def open_user_interface(self):
        # Destroy the login page
        self.root.destroy()        

        # Create the main application window
        user_root = tk.Tk()
        # Connect to the database (modify this part according to your setup)
        db_connection = userbackend.connect_to_database()
        # Create an instance of the App class from user.py
        app = App(user_root, db_connection)
        user_root.mainloop()

    

    def open_registration_page(self):
        # Create a new window for registration
        registration_window = tk.Toplevel(self.root)
        registration_window.title("Registration Page")
        registration_window.geometry("400x300")

        # Set the minimum size and make the window non-resizable
        registration_window.minsize(400, 300)
        registration_window.resizable(False, False)

        # Create a frame for better organization
        registration_frame = ttk.Frame(registration_window, padding=(20, 20, 20, 20))  # Add padding to the frame
        registration_frame.pack(expand=True, fill="both")

        # Create labels and entry widgets for registration
        name_label = ttk.Label(registration_frame, text="Name:")
        name_label.grid(row=0, column=0, pady=10, sticky="w")

        self.name_entry = ttk.Entry(registration_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=10, sticky="ew")

        email_label = ttk.Label(registration_frame, text="Email:")
        email_label.grid(row=1, column=0, pady=10, sticky="w")

        self.email_entry = ttk.Entry(registration_frame, width=30)
        self.email_entry.grid(row=1, column=1, pady=10, sticky="ew")

        phone_number_label = ttk.Label(registration_frame, text="Phone Number:")
        phone_number_label.grid(row=2, column=0, pady=10, sticky="w")

        self.phone_number_entry = ttk.Entry(registration_frame, width=30)
        self.phone_number_entry.grid(row=2, column=1, pady=10, sticky="ew")

        user_id_registration_label = ttk.Label(registration_frame, text="User ID:")
        user_id_registration_label.grid(row=3, column=0, pady=10, sticky="w")

        self.user_id_registration_entry = ttk.Entry(registration_frame, width=30)
        self.user_id_registration_entry.grid(row=3, column=1, pady=10, sticky="ew")

        password_registration_label = ttk.Label(registration_frame, text="Password:")
        password_registration_label.grid(row=4, column=0, pady=10, sticky="w")

        self.password_registration_entry = ttk.Entry(registration_frame, show="*", width=30)
        self.password_registration_entry.grid(row=4, column=1, pady=10, sticky="ew")

        # Create a register button
        register_button1 = ttk.Button(registration_frame, text="Register", command=self.register)
        register_button1.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        self.registration_window = registration_window

        # Center the frame on the screen
        registration_frame.columnconfigure(0, weight=1)  # Make the first column expandable
        registration_frame.columnconfigure(1, weight=1)  # Make the second column expandable
        registration_frame.rowconfigure(5, weight=1)  # Make the sixth row expandable
    

    def register(self):
        # Get the entered registration details
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone_number = self.phone_number_entry.get()
        user_id_registration = self.user_id_registration_entry.get()
        password_registration = self.password_registration_entry.get()

        # Check if any field is empty
        if not all([name, email, phone_number, user_id_registration, password_registration]):
            messagebox.showerror("Registration Failed", "Please fill in all fields.")
            return

        try:
            # Store the registration details in the user_registration table
            self.user_backend.register_user(name, email, phone_number, user_id_registration, password_registration)
            messagebox.showinfo("Registration Successful", "Registration successful! You can now log in.")
            # Destroy the registration window
            self.registration_window.destroy()
        except Exception as e:
            messagebox.showerror("Registration Failed", f"Registration failed. {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    db_connection = userbackend.connect_to_database()
    login_page = LoginPage(root)
    root.mainloop()
