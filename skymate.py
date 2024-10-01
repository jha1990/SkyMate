import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import time

class FlightStatusChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("SkyMate - Flight Status Checker")
        self.root.geometry("800x600") 
        self.root.configure(bg="#f0f8ff")

        self.background_image = Image.open("/Users/rajnishjha/Desktop/SkyMate/air.jpg")
        self.background_image = self.background_image.resize((800, 600), Image.LANCZOS)  
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.bg_label = tk.Label(self.root, image=self.background_photo)
        self.bg_label.place(x=0, y=150, relwidth=1, relheight=1) 

        # Flight Data
        self.flight_data = {
            "QT101": {"departure": "Delhi", "arrival": "Mumbai", "status": "On Time"},
            "QT102": {"departure": "Bengaluru", "arrival": "Delhi", "status": "Delayed"},
            "QT103": {"departure": "Mumbai", "arrival": "Chennai", "status": "On Time"},
            "QT104": {"departure": "Kolkata", "arrival": "Delhi", "status": "Cancelled"},
            "QT105": {"departure": "Chennai", "arrival": "Bengaluru", "status": "On Time"},
        }

        self.header_label = tk.Label(self.root, text="Welcome to SkyMate!", font=("Roboto", 36, "bold"), bg="#f0f8ff", fg="#2e8b57")
        self.header_label.pack(pady=20)

        self.username_var = tk.StringVar(value="Enter your name")
        self.username_entry = tk.Entry(self.root, textvariable=self.username_var, font=("Roboto", 18), width=50)
        self.username_entry.bind("<FocusIn>", self.clear_username_placeholder)
        self.username_entry.bind("<FocusOut>", self.set_username_placeholder)
        self.username_entry.pack(pady=10)

        self.flight_number_var = tk.StringVar(value="Enter flight number (e.g., QT101)")
        self.flight_number_entry = tk.Entry(self.root, textvariable=self.flight_number_var, font=("Roboto", 18), width=50)
        self.flight_number_entry.bind("<FocusIn>", self.clear_flight_placeholder)
        self.flight_number_entry.bind("<FocusOut>", self.set_flight_placeholder)
        self.flight_number_entry.pack(pady=10)

        self.departure_var = tk.StringVar(value="From (e.g., Delhi)")
        self.departure_entry = tk.Entry(self.root, textvariable=self.departure_var, font=("Roboto", 18), width=50)
        self.departure_entry.bind("<FocusIn>", self.clear_departure_placeholder)
        self.departure_entry.bind("<FocusOut>", self.set_departure_placeholder)
        self.departure_entry.pack(pady=10)

        self.arrival_var = tk.StringVar(value="To (e.g., Mumbai)")
        self.arrival_entry = tk.Entry(self.root, textvariable=self.arrival_var, font=("Roboto", 18), width=50)
        self.arrival_entry.bind("<FocusIn>", self.clear_arrival_placeholder)
        self.arrival_entry.bind("<FocusOut>", self.set_arrival_placeholder)
        self.arrival_entry.pack(pady=10)

        self.status_button = tk.Button(self.root, text="Check Flight Status", command=self.initiate_checking, font=("Roboto", 20, "bold"), bg="white", fg="black", borderwidth=2, relief="raised", padx=15, pady=10)
        self.status_button.pack(pady=20) 

        self.loading_label = tk.Label(self.root, text="", font=("Roboto", 24), bg="#f0f8ff", fg="#2e8b57")
        self.loading_label.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Roboto", 18), bg="#f0f8ff", fg="#2e8b57")
        self.result_label.pack(pady=10) 

        self.powered_by_label = tk.Label(self.root, text="Powered by Akasa Air", font=("Roboto", 14, "italic"), bg="#f0f8ff", fg="#2e8b57")
        self.powered_by_label.pack(side=tk.BOTTOM, pady=20)

        self.username_var.trace("w", self.validate_input)
        self.flight_number_var.trace("w", self.validate_input)
        self.departure_var.trace("w", self.validate_input)
        self.arrival_var.trace("w", self.validate_input)

    def initiate_checking(self):
        self.loading_label.config(text="Checking flight status...")
        self.result_label.config(text="")
        threading.Thread(target=self.check_flight_status).start()

    def check_flight_status(self):
        time.sleep(1) 
        username = self.username_var.get().strip()
        flight_number = self.flight_number_var.get().strip()
        departure_location = self.departure_var.get().strip()
        arrival_location = self.arrival_var.get().strip()

        print(f"Checking status for: {flight_number} by {username} from {departure_location} to {arrival_location}")

        if not username or username == "Enter your name":
            self.display_error("Please enter your name.")
            return

        if not flight_number or flight_number == "Enter flight number (e.g., QT101)":
            self.display_error("Please enter a flight number.")
            return

        if not departure_location or departure_location == "From (e.g., Delhi)":
            self.display_error("Please enter a departure location.")
            return

        if not arrival_location or arrival_location == "To (e.g., Mumbai)":
            self.display_error("Please enter a destination location.")
            return

        flight_info = self.flight_data.get(flight_number.upper())
        if flight_info and flight_info['departure'].lower() == departure_location.lower() and flight_info['arrival'].lower() == arrival_location.lower():
            result_text = f"Hello {username}! Your flight from {flight_info['departure']} to {flight_info['arrival']} is {flight_info['status']}."
        else:
            result_text = f"Sorry {username}, no flight found with the number {flight_number} from {departure_location} to {arrival_location}."

        print(f"Result: {result_text}") 
        self.loading_label.config(text="")
        self.result_label.config(text=result_text)

    def display_error(self, message):
        self.loading_label.config(text="")
        messagebox.showwarning("Input Error", message)

    def clear_username_placeholder(self, event):
        if self.username_var.get() == "Enter your name":
            self.username_var.set("")

    def set_username_placeholder(self, event):
        if not self.username_var.get():
            self.username_var.set("Enter your name")

    def clear_flight_placeholder(self, event):
        if self.flight_number_var.get() == "Enter flight number (e.g., QT101)":
            self.flight_number_var.set("")

    def set_flight_placeholder(self, event):
        if not self.flight_number_var.get():
            self.flight_number_var.set("Enter flight number (e.g., QT101)")

    def clear_departure_placeholder(self, event):
        if self.departure_var.get() == "From (e.g., Delhi)":
            self.departure_var.set("")

    def set_departure_placeholder(self, event):
        if not self.departure_var.get():
            self.departure_var.set("From (e.g., Delhi)")

    def clear_arrival_placeholder(self, event):
        if self.arrival_var.get() == "To (e.g., Mumbai)":
            self.arrival_var.set("")

    def set_arrival_placeholder(self, event):
        if not self.arrival_var.get():
            self.arrival_var.set("To (e.g., Mumbai)")

    def validate_input(self, *args):
        username = self.username_var.get().strip()
        flight_number = self.flight_number_var.get().strip()
        departure_location = self.departure_var.get().strip()
        arrival_location = self.arrival_var.get().strip()
        if (username and username != "Enter your name" and
                flight_number and flight_number != "Enter flight number (e.g., QT101)" and
                departure_location and departure_location != "From (e.g., Delhi)" and
                arrival_location and arrival_location != "To (e.g., Mumbai)"):
            self.status_button.config(state=tk.NORMAL)
        else:
            self.status_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = FlightStatusChecker(root)
    root.mainloop()
