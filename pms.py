# test_final.py

import customtkinter as ctk
import csv
from datetime import datetime, date
import random
import os
import json
from tkinter import messagebox, ttk, StringVar, END, PhotoImage 
import tkinter as tk
import re
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image, ImageTk
import io
import webbrowser
from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkImage, CTkCanvas, CTkComboBox, CTkEntry, CTkOptionMenu, CTkToplevel, IntVar, StringVar
from dateutil.relativedelta import relativedelta
from CTkListbox import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv, set_key, dotenv_values
#imported opencv
import pywhatkit as kit
import pyautogui
import time
import turtle

class EnvEditorApp(ctk.CTk):
    def __init__(self, env_file_path, master=None):
        super().__init__()
        self.env_file_path = env_file_path
        self.master = master

        dotenv_path = os.path.expanduser("F:/ParkingManagement/.data/.env")
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        else:
            print(f".env file does not exist at path: {dotenv_path}")

        self.json_file_path = os.path.expanduser("F:/ParkingManagement/.data/employee_data.json")

        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = os.getenv('SMTP_PORT')
        self.email_address = os.getenv('PMS_EMAIL_ADDRESS')
        self.email_password = os.getenv('PMS_EMAIL_PASSWORD')

        self.title("Environment Variable Editor")

        self.gst_no_label = ctk.CTkLabel(self, text="GST NO:")
        self.gst_no_label.grid(row=0, column=0, padx=10, pady=10)
        self.gst_no_entry = ctk.CTkEntry(self)
        self.gst_no_entry.grid(row=0, column=1, padx=10, pady=10)
        self.gst_no_entry.insert(0, os.getenv('GST_NO_VAR', ''))

        self.smtp_server_label = ctk.CTkLabel(self, text="SMTP Server:")
        self.smtp_server_label.grid(row=1, column=0, padx=10, pady=10)
        self.smtp_server_entry = ctk.CTkEntry(self)
        self.smtp_server_entry.grid(row=1, column=1, padx=10, pady=10)
        self.smtp_server_entry.insert(0, os.getenv('SMTP_SERVER', ''))

        self.smtp_port_label = ctk.CTkLabel(self, text="SMTP Port:")
        self.smtp_port_label.grid(row=2, column=0, padx=10, pady=10)
        self.smtp_port_entry = ctk.CTkEntry(self)
        self.smtp_port_entry.grid(row=2, column=1, padx=10, pady=10)
        self.smtp_port_entry.insert(0, os.getenv('SMTP_PORT', ''))

        self.email_address_label = ctk.CTkLabel(self, text="Email Address:")
        self.email_address_label.grid(row=3, column=0, padx=10, pady=10)
        self.email_address_entry = ctk.CTkEntry(self)
        self.email_address_entry.grid(row=3, column=1, padx=10, pady=10)
        self.email_address_entry.insert(0, os.getenv('PMS_EMAIL_ADDRESS', ''))

        self.email_password_label = ctk.CTkLabel(self, text="Email Password:")
        self.email_password_label.grid(row=4, column=0, padx=10, pady=10)
        self.email_password_entry = ctk.CTkEntry(self, show='*')
        self.email_password_entry.grid(row=4, column=1, padx=10, pady=10)
        self.email_password_entry.insert(0, os.getenv('PMS_EMAIL_PASSWORD', ''))

        self.eye_button = ctk.CTkButton(
            master=self,
            text="👁️",
            command=self.toggle_password,  # Assuming this method exists
            width=5,
            height=20, # To match the button's appearance with the image
        )
        self.eye_button.grid(row=4, column=2, padx=10, pady=10)

        self.num_levels_label = ctk.CTkLabel(self, text="No of Levels:")
        self.num_levels_label.grid(row=5, column=0, padx=10, pady=10)
        self.num_levels_entry = ctk.CTkEntry(self)
        self.num_levels_entry.grid(row=5, column=1, padx=10, pady=10)
        self.num_levels_entry.insert(0, os.getenv('NUM_LEVELS', ''))

        self.slots_per_level_label = ctk.CTkLabel(self, text="Slots Per Level:")
        self.slots_per_level_label.grid(row=6, column=0, padx=10, pady=10)
        self.slots_per_level_entry = ctk.CTkEntry(self)
        self.slots_per_level_entry.grid(row=6, column=1, padx=10, pady=10)
        self.slots_per_level_entry.insert(0, os.getenv('SLOT_PER_LEVEL', ''))

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_env_vars)
        self.save_button.grid(row=7, columnspan=2, pady=10)

        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_action)
        self.cancel_button.grid(row=8, columnspan=2, pady=10)

        self.password_visible = False

    def extract_info_from_json(self):

        with open(self.json_file_path, 'r') as file:
            data = json.load(file)
            owner_email = data.get('owner_email')
            employee_id = data.get('employee_id')
            employee_name = data.get('employee_name')
        return owner_email, employee_id, employee_name

    def cancel_action(self):
        self.destroy()

    def toggle_password(self):
        if self.password_visible:
            self.email_password_entry.configure(show='*')
        else:
            self.email_password_entry.configure(show='')
        self.password_visible = not self.password_visible

#     def save_env_vars(self):
#         changes_made = False

#         current_values = {
#             'GST_NO_VAR': self.gst_no_entry.get(),
#             'SMTP_SERVER': self.smtp_server_entry.get(),
#             'SMTP_PORT': self.smtp_port_entry.get(),
#             'PMS_EMAIL_ADDRESS': self.email_address_entry.get(),
#             'PMS_EMAIL_PASSWORD': self.email_password_entry.get(),
#             'NUM_LEVELS': self.num_levels_entry.get(),
#             'SLOT_PER_LEVEL': self.slots_per_level_entry.get()
#         }

#         changes = []
#         for key, current_value in current_values.items():
#             if current_value != self.original_env.get(key, ''):
#                 set_key(self.env_file_path, key, current_value)
#                 changes_made = True
#                 changes.append(f"{key}: {self.original_env.get(key, '')} -> {current_value}")

#         if changes_made:
#             body_text = f"""Dear {employee_name},

# We have received a request to make changes in your confidentional information. If this was not you, please change your password immediately.

# here are the changes:

# {'\n'.join(changes)}

# Here is your OTP: {otp}

# This is an autogenerated email sent to you by the PMS system.
# """

#             self.send_notification_via_email(owner_email, otp, employee_name, body_text)
#             messagebox.showinfo("Success", "Environment variables updated successfully!")
#         else:
#             messagebox.showinfo("Info", "No changes made.")

#     def send_notification_via_email(self):
#         """Send OTP and confirmation email to the user"""
#         try:
#             # Check if email_address and email_password are loaded correctly
#             if not self.email_address or not self.email_password:
#                 raise ValueError("Email address or password not loaded correctly from environment variables.")

            
#             msg = MIMEMultipart()
#             msg['From'] = self.email_address
#             msg['To'] = owner_email
#             msg['Subject'] = 'Confirm Information Change'
#             msg.attach(MIMEText(body_text, 'plain'))

#             server = smtplib.SMTP(self.smtp_server, self.smtp_port)
#             server.starttls()
#             server.login(self.email_address, self.email_password)
#             text = msg.as_string()
#             server.sendmail(self.email_address, owner_email, text)
#             server.quit()
#             print(f"Confirmation email sent to {owner_email}")
#         except Exception as e:
#             print(f"Error sending confirmation email: {e}")

    def save_env_vars(self, employee_name, owner_email, otp):
        changes_made = False
    
        current_values = {
            'GST_NO_VAR': self.gst_no_entry.get(),
            'SMTP_SERVER': self.smtp_server_entry.get(),
            'SMTP_PORT': self.smtp_port_entry.get(),
            'PMS_EMAIL_ADDRESS': self.email_entry.get(),
            'PMS_EMAIL_PASSWORD': self.password_entry.get(),
            'NUM_LEVELS': self.num_levels_entry.get(),
            'SLOTS_PER_LEVEL': self.slots_per_level_entry.get()
        }
    
        changes = []
        for key, current_value in current_values.items():
            if current_value != os.getenv(key, ''):
                os.environ[key] = current_value
                changes_made = True
                changes.append(f"{key}: {os.getenv(key, '')} -> {current_value}")
    
        if changes_made:
            body_text = f"""Dear {employee_name},
    
            We have received a request to make changes in your confidential information. If this was not you, please change your password immediately.
    
            Here are the changes:
    
            {'\n'.join(changes)}
    
            Here is your OTP: {otp}
    
            This is an autogenerated email sent to you by the PMS system.
            """
    
            self.send_otp_via_email(owner_email, otp, employee_name, body_text)
            messagebox.showinfo("Success", "Environment variables updated successfully!")
        else:
            messagebox.showinfo("Info", "No changes made.")
    
    def send_otp_via_email(self, owner_email, otp, employee_name, body_text):
        try:
            msg = MIMEMultipart()
            msg['From'] = os.getenv('PMS_EMAIL_ADDRESS')
            msg['To'] = owner_email
            msg['Subject'] = 'Confirm Information Change'
            msg.set_content(body_text)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(os.getenv('PMS_EMAIL_ADDRESS'), os.getenv('PMS_EMAIL_PASSWORD'))
                server.send_message(msg)

            print(f"Confirmation email sent to {owner_email}")
        except Exception as e:
            print(f"Error sending confirmation email: {e}")


    def generate_otp(self):
        """Generate a 6-digit OTP"""
        return str(random.randint(100000, 999999))

    def send_otp(self, employee_id, new_password):
        if not self.current_user_instance.get_user():
            print("No user logged in.")
            return

        if employee_id not in self.users:
            print("Employee ID not found.")
            return

        otp = self.generate_otp()
        email = self.users[employee_id].get('email')
        if email:
            self.send_otp_via_email(email, otp, self.users[employee_id]['name'], self.current_user_instance.get_user()['role'], self.current_user_instance.get_user()['name'])
        else:
            print("No email found for the employee.")

        self.users[employee_id]['otp'] = otp
        self.users[employee_id]['new_password'] = new_password  # Removed assignment of new_password
        self.save_user_data()




class OwnerPortal(CTk):
    def __init__(self, employee_management, employee_file_path):
        super().__init__()
        self.title("Owner Portal")
        self.geometry("450x600")
        self.employee_management = employee_management
        self.after_id = None
        self.current_user_instance = CurrentUser.get_instance()
        self.employee_file_path = employee_file_path
        self.users = self.load_users_from_json(self.employee_file_path)
        self.grid_columnconfigure(0, weight=1)

        self.add_employee_button = CTkButton(self, text="Add Employee", command=self.add_employee)
        self.add_employee_button.grid(row=0, column=0, padx=10, pady=(20, 5))

        self.remove_employee_button = CTkButton(self, text="Remove Employee", command=self.remove_employee)
        self.remove_employee_button.grid(row=1, column=0, padx=10, pady=(20, 5))

        self.show_employee_button = CTkButton(self, text="Show Employees", command=self.show_employees)
        self.show_employee_button.grid(row=2, column=0, padx=10, pady=(20, 5))

        self.open_pms_portal = CTkButton(self, text="Open Parking Management Portal", command=self.open_pms_p)
        self.open_pms_portal.grid(row=3, column=0, padx=10, pady=(20, 5))

        self.change_password_button = CTkButton(self, text="Change Employee Password", command=self.change_password)
        self.change_password_button.grid(row=4, column=0, padx=10, pady=(20, 5))

        self.change_details_button = CTkButton(self, text="Change Employee Details", command=self.change_details)
        self.change_details_button.grid(row=5, column=0, padx=10, pady=(20, 5))

        self.check_vehicle_records_button = CTkButton(self, text="Check Vehicle Records", command=self.check_vehicle_records)
        self.check_vehicle_records_button.grid(row=6, column=0, padx=10, pady=(20, 5))

        self.check_employee_records_button = CTkButton(self, text="Check Employee Records", command=self.check_employee_records)
        self.check_employee_records_button.grid(row=7, column=0, padx=10, pady=(20, 5))

        self.check_employee_details_changes = CTkButton(self, text="Check Changes in Employee Details", command=self.emp_details_changes)
        self.check_employee_details_changes.grid(row=8, column=0, padx=10, pady=(20, 5))

        self.change_confidential_info = CTkButton(self, text="Change Confidential Information", command=self.change_confidential_information)
        self.change_confidential_info.grid(row=9, column=0, padx=10, pady=(20, 5))

        self.logout_button = CTkButton(self, text="Logout", command=self.on_logout)
        self.logout_button.grid(row=10, column=0, padx=10, pady=(20, 5))

    def on_logout(self):
        self.destroy()
        login_window = LoginWindow(self.employee_management)
        login_window.mainloop()

    def change_details(self):
        UpdateEmployeeDetails(self.employee_management)

    def show_employees(self):
        EmployeeDetailsView(self.employee_file_path).mainloop()

    def open_pms_p(self):
        ParkingManagementSystem(self.employee_management).mainloop()


    def add_employee(self):
        self.add_window = CTkToplevel(self)
        self.add_window.title("Add Employee")
        self.add_window.geometry("450x380")

        CTkLabel(self.add_window, text="Employee ID:").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = CTkEntry(self.add_window)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        CTkLabel(self.add_window, text="Name:").grid(row=1, column=0, padx=10, pady=5)
        self.name_entry = CTkEntry(self.add_window)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        CTkLabel(self.add_window, text="Date Of Birth:").grid(row=2, column=0, padx=10, pady=5)
        self.day_var = IntVar()
        self.day_dropdown = CTkComboBox(self.add_window, values=[str(i) for i in range(1, 32)])
        self.day_dropdown.grid(row=2, column=1, padx=5, pady=2)

        self.month_var = IntVar()
        self.month_dropdown = CTkComboBox(self.add_window, values=[
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"])
        self.month_dropdown.grid(row=2, column=2, padx=5, pady=2)

        self.year_var = IntVar()
        current_year = datetime.now().year
        self.year_dropdown = CTkComboBox(self.add_window, values=[str(i) for i in range(current_year - 17, current_year - 100, -1)])
        self.year_dropdown.grid(row=3, column=1, padx=5, pady=2)

        CTkLabel(self.add_window, text="City:").grid(row=4, column=0, padx=10, pady=5)
        self.city_entry = CTkEntry(self.add_window)
        self.city_entry.grid(row=4, column=1, padx=10, pady=5)

        CTkLabel(self.add_window, text="Mobile Number:").grid(row=5, column=0, padx=10, pady=5)
        self.contact_entry = CTkEntry(self.add_window)
        self.contact_entry.grid(row=5, column=1, padx=10, pady=5)

        CTkLabel(self.add_window, text="Email :").grid(row=6, column=0, padx=10, pady=5)
        self.email_entry = CTkEntry(self.add_window)
        self.email_entry.grid(row=6, column=1, padx=10, pady=5)

        CTkLabel(self.add_window, text="Password:").grid(row=7, column=0, padx=10, pady=5)
        self.password_entry = CTkEntry(self.add_window, show="*")
        self.password_entry.grid(row=7, column=1, padx=10, pady=5)

        CTkLabel(self.add_window, text="Role").grid(row=8, column=0, padx=10, pady=5)
        roles_list = ["Select Role", "Employee", "Manager", "Co-Owner"]
        self.role = CTkOptionMenu(self.add_window, values=roles_list)
        self.role.grid(row=8, column=1, padx=10, pady=5)

        CTkLabel(self.add_window, text="Gender").grid(row=9, column=0, padx=10, pady=5)
        gender_list = ["Select Gender", "Male", "Female", "Other"]
        self.gender = CTkOptionMenu(self.add_window, values=gender_list)
        self.gender.grid(row=9, column=1, padx=10, pady=5)

        CTkButton(self.add_window, text="Submit", command=self.submit_add_employee).grid(row=10, column=1, padx=10, pady=5)
        CTkButton(self.add_window, text="Back", command=self.back_button_add).grid(row=11, column=1, padx=10, pady=5)

    def submit_add_employee(self):
        employee_id = self.username_entry.get()
        name = self.name_entry.get()
        day = int(self.day_dropdown.get())
        month = self.month_dropdown.get()
        year = int(self.year_dropdown.get())
        city = self.city_entry.get()
        contact = self.contact_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        role = self.role.get()
        gender = self.gender.get()

        if role == "Select Role":
            messagebox.showerror("Error", "Please select a valid role.")
            return

        if gender == "Select Gender":
            messagebox.showerror("Error", "Please select a valid gender.")
            return

        if not (employee_id and name and day and month and year and city and contact and password):
            messagebox.showerror("Error", "All fields must be filled.")
            return

        if employee_id in self.users:
            messagebox.showerror("Error", "Employee ID already exists. You can't add a person with the same employee ID.")
            return

        month_dict = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }
        month_number = month_dict[month]

        dob = date(year, month_number, day)
        age = self.calculate_age(dob)
        date_of_birth = f"{day} {month} {year}"

        date_of_joining = datetime.now().strftime("%d %B %Y")

        self.users[employee_id] = {
            "name": name,
            "age": age,
            "city": city,
            "contact": contact,
            "email":email,
            "password": password,
            "role": role,
            "gender": gender,
            "Date of Birth": date_of_birth,
            "Date of Joining": date_of_joining,
            "status": "active"
        }
        self.save_users_to_json(self.users)
        self.add_window.destroy()
        messagebox.showinfo("Success", "Employee added successfully.")

    def calculate_age(self, dob):
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    

    def remove_employee(self):
        self.remove_window = CTkToplevel(self)
        self.remove_window.title("Remove Employee")
        self.remove_window.geometry("450x380")

        employee_ids = list(self.users.keys())
        employee_ids.insert(0, "Select Employee")

        CTkLabel(self.remove_window, text="Employee ID:").grid(row=0, column=0, padx=10, pady=5)
        self.employee_id_var = StringVar(self.remove_window)
        self.employee_id_var.set(employee_ids[0])
        self.employee_id_dropdown = CTkOptionMenu(self.remove_window, variable=self.employee_id_var, values=employee_ids)
        self.employee_id_dropdown.grid(row=0, column=1, padx=10, pady=5)

        CTkLabel(self.remove_window, text="Type of Removal:").grid(row=1, column=0, padx=10, pady=5)
        removal_types = ["Select Type", "Removal", "Resignation"]
        self.removal_type_var = StringVar(self.remove_window)
        self.removal_type_var.set(removal_types[0]) 
        self.removal_type_dropdown = CTkOptionMenu(self.remove_window, variable=self.removal_type_var, values=removal_types)
        self.removal_type_dropdown.grid(row=1, column=1, padx=10, pady=5)

        CTkLabel(self.remove_window, text="Reason:").grid(row=2, column=0, padx=10, pady=5)
        self.removal_reason = CTkEntry(self.remove_window)
        self.removal_reason.grid(row=2, column=1, padx=10, pady=5)

        CTkButton(self.remove_window, text="Submit", command=self.submit_remove_employee).grid(row=3, column=1, padx=10, pady=10)
        CTkButton(self.remove_window, text="Back", command=self.back_button_remove).grid(row=4, column=1, padx=10, pady=10)
    
    def submit_remove_employee(self):
        employee_id = self.employee_id_var.get()
        removal_type = self.removal_type_var.get()
        removal_reason = self.removal_reason.get()

        if employee_id == "Select Employee":
            messagebox.showerror("Error", "Please select an employee ID.")
            return

        if removal_type == "Select Type":
            messagebox.showerror("Error", "Please select a removal type.")
            return

        if not removal_reason:
            messagebox.showerror("Error", "Please enter a removal reason.")
            return

        if employee_id in self.users:
            emp_details = self.users[employee_id]
            if emp_details.get("status") in ["Removal", "Resignation"]:
                if ["Removal"]:
                    message = "is already removed from this organization"
                elif ["Resignation"]:
                    message = "has already resigned from this organization"
                reason_rr = emp_details.get("reason")
                messagebox.showerror("Error", f"Employee ID '{employee_id}' {message}\nFor the reason {reason_rr}.")
                return

            details_str = (
                f"Name: {emp_details.get('name', 'N/A')}\n"
                f"Age: {emp_details.get('age', 'N/A')}\n"
                f"City: {emp_details.get('city', 'N/A')}\n"
                f"Contact: {emp_details.get('contact', 'N/A')}\n"
                f"Email: {emp_details.get('email', 'N/A')}\n"
                f"Date of Birth: {emp_details.get('Date of Birth', 'N/A')}\n"
                f"Date of Joining: {emp_details.get('Date of Joining', 'N/A')}\n"
            )

            role = emp_details.get("role")
            if role != "Owner":
                confirmation = messagebox.askyesno("Confirm", f"Are you sure you want to change the status of {employee_id} to {removal_type}?\n\nDetails:\n{details_str}\nReason: {removal_reason}")
                if confirmation:
                    self.users[employee_id]["status"] = removal_type
                    self.users[employee_id]["reason"] = removal_reason
                    today_date = datetime.now().strftime("%d %B %Y")
                    self.users[employee_id][f"date_of_{removal_type.lower()}"] = today_date
                    self.users[employee_id]["removed_by"] = self.current_user_instance.get_user().get('employee_id')
                    self.save_users_to_json(self.users)
                    self.remove_window.destroy()
                    messagebox.showinfo("Success", f"Employee status updated to {removal_type} successfully by {self.current_user_instance.get_user().get('employee_id')}.")
            else:
                messagebox.showerror("Error", "You cannot remove the owner.")
        else:
            messagebox.showerror("Error", f"Employee ID '{employee_id}' not found. They are not part of your organization.")
                
    def back_button_add(self):
        self.add_window.destroy()

    def back_button_remove(self):
        self.remove_window.destroy()

    def change_password(self):

        self.changepassword = CTkToplevel(self)
        self.changepassword.title("Change Password")
        self.changepassword.geometry("450x380")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        employee_ids = list(self.users.keys())
        employee_ids.insert(0, "Select Employee")

        CTkLabel(self.changepassword, text="Employee ID:").grid(row=0, column=1, padx=10, pady=5)
        self.employee_id_var = StringVar(self.changepassword)
        self.employee_id_var.set(employee_ids[0])
        self.employee_id_dropdown = CTkOptionMenu(self.changepassword, variable=self.employee_id_var, values=employee_ids)
        self.employee_id_dropdown.grid(row=0, column=2, padx=10, pady=5)

        ctk.CTkLabel(self.changepassword, text="New Password:").grid(row=1, column=1, padx=10, pady=5, sticky="e")
        self.new_password_entry = ctk.CTkEntry(self.changepassword, placeholder_text="New Password", show="*")
        self.new_password_entry.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        self.eye_button = ctk.CTkButton(
            master=self.changepassword,
            text="👀👁️‍🗨️",
            command=self.toggle_password,  # Assuming this method exists
            width=5,
            height=20, # To match the button's appearance with the image
        )
        self.eye_button.grid(row=1, column=3, padx=10, pady=10)

        self.send_otp_button = ctk.CTkButton(self.changepassword, text="Send OTP", command=self.send_otp)
        self.send_otp_button.grid(row=2, column=2, padx=10, pady=5)

        ctk.CTkLabel(self.changepassword, text="Enter OTP:").grid(row=3, column=1, padx=10, pady=5, sticky="e")
        self.otp_entry = ctk.CTkEntry(self.changepassword, placeholder_text="OTP")
        self.otp_entry.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        self.verify_otp_button = ctk.CTkButton(self.changepassword, text="Verify OTP", command=self.verify_otp)
        self.verify_otp_button.grid(row=4, column=2, padx=10, pady=5)

        self.status_label = ctk.CTkLabel(self.changepassword, text="")
        self.status_label.grid(row=6, column=1, columnspan=2, pady=10)

        self.cancel_button = ctk.CTkButton(self.changepassword, text="Cancel", command=self.back_button_cancel)
        self.cancel_button.grid(row=5, column=2, padx=10, pady=5)

        self.password_visible = False

    def toggle_password(self):
        if self.password_visible:
            self.new_password_entry.configure(show='*')
        else:
            self.new_password_entry.configure(show='')
        self.password_visible = not self.password_visible

    def back_button_cancel(self):
        self.changepassword.destroy()

    def send_otp(self):
        employee_id = self.employee_id_dropdown.get()
        new_password = self.new_password_entry.get()
        self.employee_management.change_password(employee_id, new_password)

    def verify_otp(self):
        employee_id = self.employee_id_dropdown.get()
        otp = self.otp_entry.get()
        if self.employee_management.verify_otp_and_update_password(employee_id, otp):
            messagebox.showinfo("Success", "Password updated successfully")
        else:
            messagebox.showerror("Error", "Invalid OTP")

    def update_employee_status(self, employee_id, new_status):
        if employee_id in self.users:
            self.users[employee_id]["status"] = new_status
            self.save_users_to_json(self.users)
            messagebox.showinfo("Success", f"Status updated to {new_status} for employee {employee_id}.")
        else:
            messagebox.showerror("Error", "Employee ID not found.")

    def show_tax_collected_today(self):
        tax_file_path = os.path.expanduser("F:/ParkingManagement/.data/tax_collected.csv")
        today = datetime.now().strftime("%d-%m-%Y")
        total_tax = 0
        try:
            with open(tax_file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Date"] == today:
                        total_tax += int(row["Tax"])

            messagebox.showinfo("Tax Collected Today", f"Total tax collected today: {total_tax}")
        except FileNotFoundError:
            messagebox.showerror("Error", "Tax collection file not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_vehicle_records(self):
        csv_file_path = r"F:/ParkingManagement/Logs/removed_vehicles.csv"
        os.system(f'start "" "{csv_file_path}"')

    def check_employee_records(self):
        csv_file_path = r"F:/ParkingManagement/Logs/employee_records.csv"
        os.system(f'start "" "{csv_file_path}"')

    def change_confidential_information(self):
        dotenv_path = os.path.expanduser("F:/ParkingManagement/.data/.env")
        EnvEditorApp(dotenv_path).mainloop()

    def emp_details_changes(self):
        csv_file_path = r"F:/ParkingManagement/Logs/employee_changes_log.csv"
        os.system(f'start "" "{csv_file_path}"')

    def load_users_from_json(self, employee_file_path):
        try:
            with open(employee_file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def save_users_to_json(self, users):
        with open(self.employee_file_path, 'w') as file:
            json.dump(users, file, indent=4)

class EmployeeDetailsView(CTk):
    def __init__(self, employee_file_path):
        super().__init__()
        self.employee_file_path = employee_file_path
        # Load data from JSON file
        with open(self.employee_file_path) as f:
            self.employees = json.load(f)

        # Create the main window
        self.title("Employee Roles and IDs")
        self.geometry("400x300")

        # Create a listbox to display roles
        self.roles_listbox = CTkListbox(self)
        unique_roles = set()
        for emp_details in self.employees.values():
            role = emp_details["role"]
            unique_roles.add(role)

        for role in unique_roles:
            self.roles_listbox.insert(ctk.END, role)
        self.roles_listbox.pack()

        # Create a frame to hold the employee ID buttons
        self.employee_id_frame = CTkFrame(self)
        self.employee_id_frame.pack(fill=ctk.BOTH, expand=True)

        # Create a Cancel button
        self.cancel_button = CTkButton(self, text="Cancel", command=self.cancel)
        self.cancel_button.pack()

        # Bind click event to the listbox
        self.roles_listbox.bind("<<ListboxSelect>>", self.on_click)

    def show_employee_ids(self, role):
        # Clear previous buttons
        for button in self.employee_id_frame.winfo_children():
            button.destroy()

        employee_ids = [emp_id for emp_id, emp_details in self.employees.items() if emp_details["role"] == role]

        for emp_id in employee_ids:
            button = CTkButton(self.employee_id_frame, text=emp_id, command=lambda emp_id=emp_id: self.show_employee_details(emp_id))
            button.pack(pady=2)

    def show_employee_details(self, emp_id):
        emp_details = self.employees[emp_id]
        details_str1 = (
            f"Name: {emp_details.get('name', 'N/A')}\n"
            f"Age: {emp_details.get('age', 'N/A')}\n"
            f"City: {emp_details.get('city', 'N/A')}\n"
            f"Contact: {emp_details.get('contact', 'N/A')}\n"
            f"Email: {emp_details.get('email', 'N/A')}\n"
            f"gender: {emp_details.get('gender', 'N/A')}\n"
            f"Date of Birth: {emp_details.get('Date of Birth', 'N/A')}\n"
            f"Date of Joining: {emp_details.get('Date of Joining', 'N/A')}\n"
            f"status: {emp_details.get('status', 'N/A')}\n"
        )

        details_str2 = details_str1  # Initialize with details_str1
    
        if emp_details.get('status') == 'Removal':
            details_str2 += (
                f"Reason: {emp_details.get('reason', 'N/A')}\n"
                f"Date of Removal: {emp_details.get('date_of_removal', 'N/A')}\n"
            )
        elif emp_details.get('status') == 'Resignation':
            details_str2 += (
                f"Reason: {emp_details.get('reason', 'N/A')}\n"
                f"Date of Resignation: {emp_details.get('date_of_resignation', 'N/A')}\n"
            )

        messagebox.showinfo("Employee Details", details_str2)

    def cancel(self):
        self.destroy()

    def on_click(self, event):
        widget = event.widget
        selection = widget.curselection()
        if isinstance(selection, tuple) and selection:
            index = selection[0]
            role = widget.get(index)
            self.show_employee_ids(role)
        elif isinstance(selection, int):
            role = widget.get(selection)
            self.show_employee_ids(role)
        else:
            print("No role selected.")  # Optional: Handle no selection scenario

class EmployeeManagement:
    def __init__(self, employee_file_path):
        self.employee_file_path = employee_file_path
        self.login_log_file_path = os.path.expanduser("F:/ParkingManagement/.data/punch_in_data.json")
        self.logout_log_file_path = os.path.expanduser("F:/ParkingManagement/logs/employee_records.csv")
        self.users = self.load_user_data()
        self.current_user_instance = CurrentUser.get_instance()

        # Load environment variables from .env file
        dotenv_path = os.path.expanduser("F:/ParkingManagement/.data/.env")
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        else:
            print(f".env file does not exist at path: {dotenv_path}")

        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = os.getenv('SMTP_PORT')
        self.email_address = os.getenv('PMS_EMAIL_ADDRESS')
        self.email_password = os.getenv('PMS_EMAIL_PASSWORD')

    def load_user_data(self):
        if os.path.exists(self.employee_file_path):
            with open(self.employee_file_path, 'r') as file:
                print("User data loaded successfully")  # Debug statement
                return json.load(file)
        else:
            print("User data file does not exist")  # Debug statement
            return {}

    def save_user_data(self):
        with open(self.employee_file_path, 'w') as file:
            json.dump(self.users, file, indent=4)
            print("User data saved successfully")  # Debug statement

    def generate_otp(self):
        """Generate a 6-digit OTP"""
        return str(random.randint(100000, 999999))

    def send_otp_via_email(self, email, otp, employee_name, current_role, current_employee):
        """Send OTP and confirmation email to the user"""
        try:
            # Check if email_address and email_password are loaded correctly
            if not self.email_address or not self.email_password:
                raise ValueError("Email address or password not loaded correctly from environment variables.")

            body_text = f"""Dear {employee_name},

We have received a request to change your password. If this was not you, please contact the {current_role} {current_employee} immediately.

Here is your OTP: {otp}

This is an autogenerated email sent to you by the PMS system.
"""

            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = email
            msg['Subject'] = 'Confirm Password Change'
            msg.attach(MIMEText(body_text, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_address, self.email_password)
            text = msg.as_string()
            server.sendmail(self.email_address, email, text)
            server.quit()
            print(f"Confirmation email sent to {email}")
        except Exception as e:
            print(f"Error sending confirmation email: {e}")

    def send_otp(self, employee_id, new_password):
        if not self.current_user_instance.get_user():
            print("No user logged in.")
            return

        if employee_id not in self.users:
            print("Employee ID not found.")
            return

        otp = self.generate_otp()
        email = self.users[employee_id].get('email')
        if email:
            self.send_otp_via_email(email, otp, self.users[employee_id]['name'], self.current_user_instance.get_user()['role'], self.current_user_instance.get_user()['name'])
        else:
            print("No email found for the employee.")

        self.users[employee_id]['otp'] = otp
        self.users[employee_id]['new_password'] = new_password  # Removed assignment of new_password
        self.save_user_data()

    def change_password(self, employee_id, new_password):
        if not self.current_user_instance.get_user():
            print("No user logged in.")
            return

        if self.current_user_instance.get_user()['role'] == 'Owner' and employee_id == 'owner_id':
            print("Cannot change Owner's password.")
            return
        
        print(f"Current user: {self.current_user_instance.get_user()}")  # Debug statement

        if employee_id not in self.users:
            print("Employee ID not found.")
            return

        email = self.users[employee_id].get('email')
        if email:
            self.send_otp(employee_id, new_password)
            messagebox.showinfo("Password Change", "OTP sent successfully for password change.")
        else:
            print("No email found for the employee.")

    def clear_data_after_password_change(self, employee_id):
        if employee_id in self.users:
            if 'otp' in self.users[employee_id]:
                del self.users[employee_id]['otp']
            if 'new_password' in self.users[employee_id]:
                del self.users[employee_id]['new_password']
            self.save_user_data()
            print("Data cleared after password change.")

    def update_employee_details(self, employee_id, new_details):
        if employee_id in self.users:
            old_details = self.users[employee_id].copy()
            self.users[employee_id].update(new_details)
            self.save_user_data()
            self.log_changes(old_details, new_details, employee_id)
            return True
        return False

    def log_changes(self, old_details, new_details, employee_id):
        current_user_instance = CurrentUser.get_instance().get_user()
        current_user_id = current_user_instance.get('employee_id', 'Unknown') if current_user_instance else 'Unknown'
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'updated_by': current_user_id,
            'employee_id': employee_id,
            'old_details': old_details,
            'new_details': new_details
        }

        log_file = 'F:/ParkingManagement/Logs/employee_changes_log.csv'
        file_exists = os.path.isfile(log_file)

        with open(log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['timestamp', 'updated_by', 'employee_id', 'old_details', 'new_details'])
            writer.writerow([
                log_entry['timestamp'],
                log_entry['updated_by'],
                log_entry['employee_id'],
                json.dumps(log_entry['old_details']),
                json.dumps(log_entry['new_details'])
            ])

    def verify_otp_and_update_password(self, employee_id, otp):
        if not self.current_user_instance.get_user():
            print("No user logged in.")
            return False
        
        print(f"Current user: {self.current_user_instance.get_user()}")  # Debug statement

        user = self.users.get(employee_id)
        if user and user.get('otp') == otp:
            user['password'] = user['new_password']
            del user['new_password']
            del user['otp']
            self.save_user_data()
            print("Password updated successfully")
            self.clear_data_after_password_change(employee_id)
            return True
        else:
            print("Invalid OTP")
            return False

    def log_login(self, employee_id):
        login_time = datetime.now().strftime("%H:%M:%S")
        login_date = datetime.now().strftime("%d-%m-%Y")
        log_entry = {
            "employee_id": employee_id,
            "login_time": login_time,
            "login_date": login_date
        }
        print(f"Logging in: {log_entry}")  # Debug statement

        if os.path.exists(self.login_log_file_path):
            with open(self.login_log_file_path, 'r') as file:
                try:
                    login_logs = json.load(file)
                    if not isinstance(login_logs, list):
                        login_logs = []  # Ensure login_logs is a list
                    print(f"Existing login logs loaded: {login_logs}")  # Debug statement
                except json.JSONDecodeError:
                    print("JSON decode error, initializing empty log list")  # Debug statement
                    login_logs = []
        else:
            print("Log file does not exist, initializing new log list")  # Debug statement
            login_logs = []

        login_logs.append(log_entry)

        with open(self.login_log_file_path, 'w') as file:
            json.dump(login_logs, file, indent=4)
            print(f"Log entry appended: {log_entry}") 

    def log_logout(self, employee_id):
        logout_time = datetime.now().strftime("%H:%M:%S")
        logout_date = datetime.now().strftime("%d-%m-%Y")
        log_entry = {
            "employee_id": employee_id,
            "logout_time": logout_time,
            "logout_date": logout_date
        }
        print(f"Logging out: {log_entry}")  # Debug statement

        if os.path.exists(self.login_log_file_path):
            with open(self.login_log_file_path, 'r') as file:
                try:
                    login_logs = json.load(file)
                    if not isinstance(login_logs, list):
                        login_logs = []  # Ensure login_logs is a list
                    print(f"Existing login logs loaded: {login_logs}")  # Debug statement
                except json.JSONDecodeError:
                    print("JSON decode error, initializing empty log list")  # Debug statement
                    login_logs = []
        else:
            print("Log file does not exist, initializing new log list")  # Debug statement
            login_logs = []

        login_entry = next((log for log in login_logs if log["employee_id"] == employee_id), None)
        if login_entry:
            login_logs.remove(login_entry)

            with open(self.login_log_file_path, 'w') as file:
                json.dump(login_logs, file, indent=4)
                print(f"Login entry removed: {login_entry}")  # Debug statement

            if not os.path.exists(self.logout_log_file_path):
                with open(self.logout_log_file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["employee_id", "login_time", "login_date", "logout_time", "logout_date"])

            with open(self.logout_log_file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([employee_id, login_entry['login_time'], login_entry['login_date'], logout_time, logout_date])
                print(f"Logout entry appended: {log_entry}")  # Debug statement
        else:
            print(f"No login entry found for employee_id: {employee_id}")  # Debug statement

    def login(self, employee_id, password):
        user = self.users.get(employee_id)
        if user and user['password'] == password:
            user['employee_id'] = employee_id  # Ensure employee_id is set
            self.current_user_instance.set_user(user)
            self.log_login(employee_id)
            print(f"User {employee_id} logged in successfully")  # Debug statement
            print(f"Current user set to: {self.current_user_instance.get_user()}")  # Debug statement
            return user['role']
        else:
            print(f"Login failed for user {employee_id}")  # Debug statement
            return None


    def logout(self):
        if not self.current_user_instance.get_user():
            print("No user logged in.")
            return
        
        employee_id = self.current_user_instance.get_user().get('employee_id')
        if employee_id:
            self.log_logout(employee_id)
            print(f"User {employee_id} logged out successfully")  # Debug statement
        else:
            print("No employee_id found for the current user.")  # Debug statement
        self.current_user_instance.set_user(None)

class UpdateEmployeeDetails:
    def __init__(self, employee_management):
        self.employee_management = employee_management
        self.update_window = ctk.CTkToplevel()
        self.json_file = os.path.expanduser("F:/ParkingManagement/.data/employee_data.json")
        self.update_window.title("Update Employee Details")
        self.after_id = None
        self.original_details = None

        self.current_user_instance = CurrentUser.get_instance().get_user()
        if not self.current_user_instance:
            messagebox.showerror("Error", "No user logged in.")
            self.update_window.destroy()
            return

        employee_ids = list(self.employee_management.users.keys())
        employee_ids.insert(0, "Select Employee")

        ctk.CTkLabel(self.update_window, text="Employee ID:").grid(row=0, column=0, padx=10, pady=5)
        self.employee_id_var = StringVar(self.update_window)
        self.employee_id_var.set(employee_ids[0])
        self.employee_id_dropdown = ctk.CTkOptionMenu(self.update_window, variable=self.employee_id_var, values=employee_ids, command=self.populate_details)
        self.employee_id_dropdown.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(self.update_window, text="Name:").grid(row=1, column=0, padx=10, pady=10)
        self.name_entry = ctk.CTkEntry(self.update_window)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.update_window, text="Age:").grid(row=2, column=0, padx=10, pady=10)
        self.age_entry = ctk.CTkEntry(self.update_window)
        self.age_entry.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.update_window, text="City:").grid(row=3, column=0, padx=10, pady=10)
        self.city_entry = ctk.CTkEntry(self.update_window)
        self.city_entry.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.update_window, text="Contact:").grid(row=4, column=0, padx=10, pady=10)
        self.contact_entry = ctk.CTkEntry(self.update_window)
        self.contact_entry.grid(row=4, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.update_window, text="Email:").grid(row=5, column=0, padx=10, pady=10)
        self.email_entry = ctk.CTkEntry(self.update_window)
        self.email_entry.grid(row=5, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.update_window, text="Role:").grid(row=6, column=0, padx=10, pady=10)
        self.role_entry = ctk.CTkEntry(self.update_window)
        self.role_entry.grid(row=6, column=1, padx=10, pady=10)

        ctk.CTkButton(self.update_window, text="Update", command=self.update_details).grid(row=7, column=0, columnspan=2, pady=10)
        ctk.CTkButton(self.update_window, text="Cancel", command=self.back_updatedetails).grid(row=8, column=0, columnspan=2, pady=10)

    def back_updatedetails(self):
        if self.after_id is not None:
            self.after_cancel(self.after_id)
        self.update_window.destroy()

    def populate_details(self, selected_employee_id):
        if selected_employee_id == "Select Employee":
            self.clear_fields()
            return

        employee_details = self.employee_management.users.get(selected_employee_id)
        if employee_details:
            self.name_entry.delete(0, END)
            self.name_entry.insert(0, employee_details.get('name', ''))
            self.age_entry.delete(0, END)
            self.age_entry.insert(0, employee_details.get('age', ''))
            self.city_entry.delete(0, END)
            self.city_entry.insert(0, employee_details.get('city', ''))
            self.contact_entry.delete(0, END)
            self.contact_entry.insert(0, employee_details.get('contact', ''))
            self.email_entry.delete(0, END)
            self.email_entry.insert(0, employee_details.get('email', ''))
            self.role_entry.delete(0, END)
            self.role_entry.insert(0, employee_details.get('role', ''))
            self.original_details = employee_details

    def clear_fields(self):
        self.name_entry.delete(0, END)
        self.age_entry.delete(0, END)
        self.city_entry.delete(0, END)
        self.contact_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.role_entry.delete(0, END)

    def update_details(self):
        selected_employee_id = self.employee_id_var.get()
        if selected_employee_id == "Select Employee":
            messagebox.showerror("Error", "Please select an employee.")
            return

        new_details = {
            'name': self.name_entry.get(),
            'age': self.age_entry.get(),
            'city': self.city_entry.get(),
            'contact': self.contact_entry.get(),
            'email': self.email_entry.get(),
            'role': self.role_entry.get()
        }

        if new_details == self.original_details:
            if messagebox.askyesno("No Changes", "No data has changed. Are you sure you want to save?"):
                self.update_window.destroy()
                return
            else:
                return

        try:
            with open(self.json_file, 'r') as f:
                employees = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", f"JSON file '{self.json_file}' not found.")
            return
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"Invalid JSON format in '{self.json_file}'.")
            return

        employee_details = employees.get(selected_employee_id)
        if employee_details and employee_details.get('status') == 'active':
            employees[selected_employee_id].update(new_details)
            try:
                with open(self.json_file, 'w') as f:
                    json.dump(employees, f, indent=4)
                self.update_window.destroy()
                messagebox.showinfo("Success", "Details updated successfully.")
            except IOError:
                messagebox.showerror("Error", f"Failed to write to JSON file '{self.json_file}'.")
        elif employee_details:
            messagebox.showerror("Error", "You can't change data of a non-active employee.")
        else:
            messagebox.showerror("Error", f"Employee with ID '{selected_employee_id}' not found in '{self.json_file}'.")


class LoginWindow(ctk.CTk):
    def __init__(self, employee_management):
        super().__init__()

        self.title("Login Portal")
        self.geometry("400x300")
        self.employee_management = employee_management
        self.current_user_instance = CurrentUser.get_instance()
        self.employee_data = {}
        self.after_id = None

        employee_file_path = os.path.expanduser("F:/ParkingManagement/.data/employee_data.json")
        self.load_data_from_json(employee_file_path)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(self, text="Employee ID:").grid(row=0, column=1, padx=10, pady=5, sticky="e")
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self, text="Password:").grid(row=1, column=1, padx=10, pady=5, sticky="e")
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.grid(row=1, column=2, columnspan = 1, padx=10, pady=5, sticky="w")

        self.eye_button = ctk.CTkButton(
            master=self,
            text="👀",
            command=self.toggle_password,
            width=2,
            height=10,
        )
        self.eye_button.grid(row=1, column=3, padx=5, pady=10)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_user)
        self.login_button.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

        self.close_button = ctk.CTkButton(self, text="Exit", command=self.on_close)
        self.close_button.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=4, column=1, columnspan=2, pady=10)

        self.password_visible = False

    def toggle_password(self):
        if self.password_visible:
            self.password_entry.configure(show='*')
        else:
            self.password_entry.configure(show='')
        self.password_visible = not self.password_visible

    def on_close(self):
        if self.after_id is not None:
            self.after_cancel(self.after_id)  # Cancel the scheduled after event
        self.employee_management.logout()
        self.destroy()

    def load_data_from_json(self, employee_file_path):
        try:
            with open(employee_file_path, "r") as f:
                self.employee_data = json.load(f)
        except FileNotFoundError:
            print("Error: JSON file not found!")
            messagebox.showerror("Error", "Employee data file not found!")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON data: {e}")
            messagebox.showerror("Error", "Error parsing employee data file!")

    def login_user(self):
        employee_id = self.username_entry.get()
        password = self.password_entry.get()

        if not employee_id or not password:
            messagebox.showerror("Error", "Please enter both employee ID and password!")
            return

        role = self.employee_management.login(employee_id, password)
        if role:
            self.status_label.configure(text=f"Welcome {self.current_user_instance.get_user()['name']}!")
            self.show_portal(role)
        else:
            messagebox.showerror("Error", "Invalid employee ID or password!")

    def show_portal(self, role):
        employee_file_path = os.path.expanduser("F:/ParkingManagement/.data/employee_data.json")
        if role == "Owner":
            self.destroy()
            OwnerPortal(self.employee_management, employee_file_path).mainloop()
        elif role == "Manager":
            self.destroy()
            # ManagerPortal(self.employee_management).mainloop()
        elif role == "Employee":
            self.destroy()
            ParkingManagementSystem(self.employee_management).mainloop()
        else:
            print("Unauthorized access attempt.")



class ParkingManagementSystem(ctk.CTk):
    def __init__(self, employee_management):
        super().__init__()

        self.title("Parking Management System")
        self.geometry("500x400")
        self.employee_management = employee_management
        self.after_id = None
        self.current_user_instance = CurrentUser.get_instance()
        file_path = os.path.expanduser("F:/ParkingManagement/.data/parking_data.json")
        self.num_levels = int(os.getenv('NUM_LEVELS'))
        self.slots_per_level = int(os.getenv('SLOT_PER_LEVEL'))
        self.parking_slots = [None] * (self.num_levels * self.slots_per_level)
        self.update_slots_per_level
        self.vehicle_window = None 
        self.parked_vehicles = {}
        self.data_file = file_path  # JSON file to store parking data
        self.load_parking_data()

        self.schedule_vehicle_checks()

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as file:
                json.dump(self.parking_slots, file, indent=4, default=str)
            print(f"Created new JSON file at: {file_path}")
        else:
            print(f"JSON file already exists at: {file_path}")

        ctk.CTkLabel(self, text="License Plate:").grid(row=0, column=0, padx=10, pady=(20, 5))
        self.license_plate_entry = ctk.CTkEntry(self, width=200, placeholder_text="Enter License Plate")
        self.license_plate_entry.grid(row=0, column=1, padx=10, pady=(20, 5))

        ctk.CTkLabel(self, text="Mobile Number:").grid(row=1, column=0, padx=10, pady=5)
        self.mobile_number_entry = ctk.CTkEntry(self, width=200, placeholder_text="Enter Mobile Number")
        self.mobile_number_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Vehicle Type:").grid(row=2, column=0, padx=10, pady=5)
        vehicle_list = ["Select Vehicle", "Car", "Jeep", "Taxi", "Pickup-truck", "Army", "Ambulance","Police", "Other 4-wheeler"]
        self.vehicle_type = ctk.CTkOptionMenu(self, values=vehicle_list)
        self.vehicle_type.set(vehicle_list[1])
        self.vehicle_type.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Parking Level:").grid(row=3, column=0, padx=10, pady=5)
        levels = ["Select Level", "Level 1", "Level 2", "Level 3"]
        self.level_number = ctk.CTkOptionMenu(self, values=levels)
        self.level_number.set(levels[1])  # Set "Level 1" as the default option using index
        self.level_number.grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkButton(self, text="Park Vehicle", command=self.park_vehicle).grid(row=4, column=1, padx=10, pady=5)

        ctk.CTkButton(self, text="Remove Vehicle", command=self.remove_vehicle).grid(row=5, column=1, padx=10, pady=5)

        ctk.CTkButton(self, text="Show Parked Vehicles", command=self.show_parked_vehicles).grid(row=6, column=1, padx=10, pady=5)

        ctk.CTkLabel(self, text="Search Vehicle:").grid(row=7, column=0, padx=10, pady=5)
        self.search_vehicle_entry = ctk.CTkEntry(self, width=200, placeholder_text="Enter License Plate")
        self.search_vehicle_entry.grid(row=7, column=1, padx=10, pady=5)
        ctk.CTkButton(self, text="Search", command=self.search_vehicle).grid(row=7, column=2, padx=10, pady=5)

        ctk.CTkButton(self, text="Log Out", command=self.on_logout).grid(row=8, column=1, padx=10, pady=5)

    def update_slots_per_level(self):
        # Keep track of the current parked vehicles per level
        current_cars = [self.parking_slots[i:i + self.slots_per_level] for i in range(0, len(self.parking_slots), self.slots_per_level)]
        
        # Reload updated configuration from the environment
        load_dotenv(override=True)
        self.num_levels = int(os.getenv('NUM_LEVELS'))
        self.slots_per_level = int(os.getenv('SLOT_PER_LEVEL'))
        
        # Reset the parking slots while keeping existing cars intact
        self.parking_slots = []

        # Rebuild the parking slots while preserving current cars
        for level_cars in current_cars:
            if len(level_cars) > self.slots_per_level:
                # Truncate cars if the new slots per level are fewer
                self.parking_slots.extend(level_cars[:self.slots_per_level])
            else:
                # Keep the existing cars and add new empty slots (None) as needed
                self.parking_slots.extend(level_cars + [None] * (self.slots_per_level - len(level_cars)))

        # If the number of levels increased, add new empty levels
        if len(current_cars) < self.num_levels:
            for _ in range(self.num_levels - len(current_cars)):
                self.parking_slots.extend([None] * self.slots_per_level)


    
    def on_logout(self):
        self.save_parking_data()
        self.destroy()
        login_window_pms = LoginWindow(self.employee_management)
        login_window_pms.mainloop()

    def load_parking_data(self):
        try:
            with open(self.data_file, 'r') as file:
                self.parking_slots = json.load(file)
                print(f"Loaded parking data from: {self.data_file}")
        except (FileNotFoundError, json.JSONDecodeError):
            self.parking_slots = [None] * (self.num_levels * self.slots_per_level)

    def save_parking_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.parking_slots, file, indent=4, default=str)

    def park_vehicle(self):
        license_plate = self.license_plate_entry.get()
        mobile_number = self.mobile_number_entry.get()
        vehicle_type = self.vehicle_type.get()
        level = self.level_number.get()
        entry_time = datetime.now()
        entry_date = entry_time.date().strftime("%d-%m-%Y")
        entry_time_str = entry_time.time().strftime("%H:%M:%S")
        normalize_licence_plate = r'^[A-Z]{2}\d{2}[A-Z]{1}\d{4}$|^[A-Z]{2}\d{1}[A-Z]{3}\d{4}$|^[A-Z]{2}\d{2}[A4-Z]{2}\d{4}$|^\d{2}[A-Z]{1}\d{6}[A-Z]{1}$'

        if not all([license_plate, mobile_number, vehicle_type, level]):
            messagebox.showerror("Error", "Please enter all details!")
            return

        if not re.match(normalize_licence_plate, license_plate):
            messagebox.showerror("Error", "Invalid license plate format. Check the number plate.")
            return

        if not re.match(r'^\d{10}$', mobile_number):
            messagebox.showerror("Error", "Invalid mobile number. Enter 10 digits.")
            return

        if vehicle_type == "Select Vehicle":
            messagebox.showerror("Error", "Please select a vehicle type.")
            return

        if level == "Select Level":
            messagebox.showerror("Error", "Please select a parking level.")
            return

        for vehicle in self.parking_slots:
            if vehicle and vehicle['License Plate'] == license_plate:
                messagebox.showinfo("Duplicate Entry", f"Vehicle with license plate {license_plate} is already parked at {vehicle['Level']}, Slot {vehicle['Slot']}.")
                return

        # Extract level number and adjust to zero-based index
        level_index = int(level.split()[-1]) - 1
        # Determine the slot range for the given level
        start_index = level_index * self.slots_per_level
        end_index = start_index + self.slots_per_level
        try:
            # Find the first available slot within the range for the given level
            slot_index = self.parking_slots[start_index:end_index].index(None) + start_index
            # Calculate the slot number within the level (1-based indexing for user-friendly display)
            slot_number = (slot_index % self.slots_per_level) + 1
            # Assign the slot to the vehicle
            self.parking_slots[slot_index] = {
                "License Plate": license_plate,
                "Mobile Number": mobile_number,
                "Vehicle Type": vehicle_type,
                "Level": level,
                "Slot": slot_number,
                "Entry Date": entry_date,
                "Entry Time": entry_time_str
            }
            # Show success message
            messagebox.showinfo("Success", f"Vehicle parked successfully in {level}, Slot {slot_number}!")
            # Save the updated parking data
            self.save_parking_data()
        except ValueError:
            messagebox.showerror("Error", f"No available parking slots in {level}.")

        phone_no_w = mobile_number
        phone_no = "+91" + str(phone_no_w)
        message = f"⚠️Parking Alert!⚠️\nYour vehicle has been successfully parked 🚗 \n{license_plate} \n{level}\nSlot {slot_index - start_index + 1}.\nEntry Time: {datetime.now().strftime('%H:%M:%S')}\nEntry Date: {datetime.now().strftime('%d-%m-%Y')}\n At 👉 V-Park Parkings\n1234 Parking Way, Parkville 12345"
        self.send_whatsapp_message(phone_no, message)

    def send_whatsapp_message(self, phone_no, message):
        # Get current time
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute

        # Add 1 minute to the current time
        future_minute = current_minute + 1
        future_hour = current_hour

        # Handle minute overflow
        if future_minute >= 60:
            future_minute -= 60
            future_hour += 1

        # Handle hour overflow (optional, depending on the library's requirements)
        if future_hour >= 24:
            future_hour -= 24

        # Open WhatsApp Web and send the message
        kit.sendwhatmsg(phone_no, message, future_hour, future_minute)
    
        # Wait for WhatsApp Web to open
        time.sleep(5)
        
        # Send the message
        pyautogui.press('enter')

        send_image_path = os.path.expanduser("F:/ParkingManagement/requirements/send_button.png")
        if not os.path.isfile(send_image_path):
            raise FileNotFoundError(f"{send_image_path} not found.")
        send_btn = pyautogui.locateCenterOnScreen(send_image_path, confidence=0.9)
        
        if send_btn:
            pyautogui.click(send_btn)
            time.sleep(7)
        else:
            pyautogui.press('enter')
            print("Send button not found.")
        
        # Wait for the message to be sent
        time.sleep(5)
        
        # Close the browser window (assuming the browser is the active window)
        pyautogui.hotkey('ctrl', 'w')

    def send_whatsapp_document(self, phone_no, output_filename, message):
        try:
            # Open WhatsApp Web for the specified phone number
            # phone_no = "+91" + vehicle['Mobile Number']
            webbrowser.open(f"https://web.whatsapp.com/send?phone={phone_no}")
            time.sleep(20)  # Wait for WhatsApp Web to load

            # Debug statement to ensure file exists
            plus_sign_image_path = os.path.expanduser("F:/ParkingManagement/requirements/plus_sign.png")
            if not os.path.isfile(plus_sign_image_path):
                raise FileNotFoundError(f"{plus_sign_image_path} not found.")

            # Locate the plus sign icon and click it
            plus_sign_btn = pyautogui.locateCenterOnScreen(plus_sign_image_path, confidence=0.9)
            if plus_sign_btn:
                pyautogui.click(plus_sign_btn)
                time.sleep(2)
                
                # Locate the document icon and click it
                document_image_path = os.path.expanduser("F:/ParkingManagement/requirements/document_button.png")
                if not os.path.isfile(document_image_path):
                    raise FileNotFoundError(f"{document_image_path} not found.")
                document_btn = pyautogui.locateCenterOnScreen(document_image_path, confidence=0.9)
                if document_btn:
                    pyautogui.click(document_btn)
                    time.sleep(2)
                    
                    # Type the absolute path of the document and press enter
                    pyautogui.write(os.path.abspath(output_filename))
                    pyautogui.press('enter')
                    time.sleep(3)

                    # Locate the send button and click it
                    send_image_path = os.path.expanduser("F:/ParkingManagement/requirements/send_button.png")
                    if not os.path.isfile(send_image_path):
                        raise FileNotFoundError(f"{send_image_path} not found.")
                    send_btn = pyautogui.locateCenterOnScreen(send_image_path, confidence=0.9)

                    pyautogui.press('enter')
                    
                    if send_btn:
                        pyautogui.click(send_btn)
                        time.sleep(7)
                    else:
                        pyautogui.press('enter')
                        print("Send button not found.")
                else:
                    print("Document button not found.")
            else:
                print("Plus sign button not found.")
            pyautogui.hotkey('ctrl', 'w')
        except Exception as e:
            print(f"An error occurred: {e}")


    def calculate_duration(self, entry_time, exit_time):
        duration = exit_time - entry_time
        total_seconds = duration.total_seconds()
        total_hours = int(total_seconds // 3600)  # Convert seconds to hours
        minutes = int((total_seconds % 3600) // 60)  # Remaining minutes
        seconds = int(total_seconds % 60)  # Remaining seconds
        
        return total_hours, minutes, seconds

    def remove_vehicle(self):
        license_plate = self.license_plate_entry.get().strip()
        found = False
        for index, vehicle in enumerate(self.parking_slots):
            if vehicle and vehicle['License Plate'] == license_plate:
                found = True
                exit_time_o = datetime.now()
                exit_time_w = exit_time_o.time().strftime("%H:%M:%S")
                exit_date = exit_time_o.date().strftime("%d-%m-%Y")
                entry_time = datetime.strptime(f"{vehicle['Entry Date']} {vehicle['Entry Time']}", "%d-%m-%Y %H:%M:%S")
                exit_time = datetime.strptime(f"{exit_date} {exit_time_w}", "%d-%m-%Y %H:%M:%S")
                total_hours, minutes, seconds = self.calculate_duration(entry_time, exit_time)
                time_stayed = (total_hours, minutes, seconds)
                bill_without_gst, cgst, sgst = self.calculate_billing(total_hours, vehicle['Vehicle Type'])
                total_bill = bill_without_gst + cgst + sgst
                vehicle_info = {
                    "License Plate": vehicle['License Plate'],
                    "Vehicle Type": vehicle['Vehicle Type'],
                    "Mobile Number": vehicle['Mobile Number'],
                    "Level": vehicle['Level'],
                    "Slot": index + 1,  # Assuming slot index is 0-based and you want to show 1-based
                    "Entry Date": vehicle['Entry Date'],
                    "Entry Time": vehicle['Entry Time'],
                    "Exit Date": exit_date,
                    "Exit Time": exit_time_w,
                    "Duration": time_stayed,
                    "Cost": bill_without_gst,
                    "CGST": cgst,
                    "SGST": sgst,
                    "Total Cost": total_bill
                }
                self.generate_parking_receipt(vehicle_info)
                self.parking_slots[index] = None
                self.save_parking_data()
                self.log_removed_vehicle(vehicle_info, index, vehicle, entry_time, exit_time, time_stayed, total_bill)
                mob_no = "+91" + vehicle['Mobile Number']
                self.send_whatsapp_document(mob_no, output_filename, "Here's the receipt of the Parking.")

                messagebox.showinfo("Bill", f"Total bill for {license_plate} is: ₹{total_bill:.2f}")
                return
            
        if not found:
            messagebox.showerror("Error", "Vehicle not found!")

    def calculate_billing(self, hours, vehicle_type):
        
        if vehicle_type in ["Army", "Police"]:
            return 0, f"No billing for {vehicle_type} vehicles. Thank you for your service!"
        
        elif vehicle_type in ["Ambulance"]:
            return 0, f"No billing for {vehicle_type}. Thank you for your service!"
        
        else:    
            rates = [
                (3, 20),   # Rs. 20 per hour for the first 3 hours
                (6, 15),   # Rs. 15 per hour for the next 3 hours (hours 4 to 6)
                (9, 10),   # Rs. 10 per hour for the next 3 hours (hours 7 to 9)
                (24, 50/15),  # Rs. 50 flat rate for the next 15 hours (hours 10 to 24)
                (float('inf'), 100/24)  # Rs. 100 per 24 hours after 24 hours
            ]
            
            total_cost = 0
            remaining_hours = hours
            
            for limit, rate in rates:
                if remaining_hours <= 0:
                    break
                
                if remaining_hours <= limit:
                    total_cost += remaining_hours * rate
                    remaining_hours = 0
                else:
                    total_cost += limit * rate
                    remaining_hours -= limit
            
            # Additional GST calculation
            cgst = total_cost * 0.09
            sgst = total_cost * 0.09
            
            return total_cost, cgst, sgst

    def show_parked_vehicles(self):
        if self.vehicle_window is not None and self.vehicle_window.winfo_exists():
            return  # If the window exists, do nothing

        self.vehicle_window = ctk.CTkToplevel(self)
        self.vehicle_window.title("Parked Vehicles")
        self.vehicle_window.geometry("800x600")  # Increased window size

        frame = ctk.CTkFrame(self.vehicle_window)
        frame.pack(expand=True, fill='both', padx=10, pady=5)

        # Configure style for larger text
        style = ttk.Style()
        style.configure("Treeview", font=('Helvetica', 10))  # Increase font size
        style.configure("Treeview.Heading", font=('Helvetica', 14, 'bold'))  # Larger font size for headings

        # Create Treeview widget with headings
        tree = ttk.Treeview(frame, columns=("Slot", "License Plate", "Mobile Number", "Vehicle Type", "Entry Time", "Entry Date"), show="headings")
        tree.pack(side='left', fill='both', expand=True)

        # Set headings
        tree.heading("Slot", text="Slot")
        tree.heading("License Plate", text="License Plate")
        tree.heading("Mobile Number", text="Mobile Number")
        tree.heading("Vehicle Type", text="Vehicle Type")
        tree.heading("Entry Time", text="Entry Time")
        tree.heading("Entry Date", text="Entry Date")

        # Dictionary to store level nodes
        level_nodes = {}

        # Insert level nodes into treeview
        for i in range(self.num_levels):
            level = f"Level {i + 1}"
            level_node = tree.insert("", "end", text=level, values=(level, "-", "-", "-", "-", "-"))
            level_nodes[level] = level_node

        # Populate the tree with parked vehicles
        for index, vehicle in enumerate(self.parking_slots):
            level_index = (index // self.slots_per_level) + 1
            slot_number = (index % self.slots_per_level) + 1  # Slot numbering from 1 to 10
            level = f"Level {level_index}"
            slot_number = f"Slot {slot_number}"
            if vehicle:
                entry_time = datetime.strptime(vehicle["Entry Time"], "%H:%M:%S")
                entry_date = datetime.strptime(vehicle["Entry Date"], "%d-%m-%Y")
                tree.insert(level_nodes[level], "end", values=(slot_number, vehicle["License Plate"], vehicle["Mobile Number"], vehicle["Vehicle Type"], entry_time.strftime("%H:%M:%S"), entry_date.strftime("%d-%m-%Y")))
            else:
                tree.insert(level_nodes[level], "end", values=(slot_number, "-", "-", "-", "-", "-"))

        # Close button after scrollbars (adjusted for order)
        close_button = ctk.CTkButton(self.vehicle_window, text="Close", command=self.close_vehicle_window)
        close_button.pack(pady=5)


    def close_vehicle_window(self):
        if self.vehicle_window is not None and self.vehicle_window.winfo_exists():
            self.vehicle_window.destroy()
            self.vehicle_window = None


    def search_vehicle(self):
        license_plate = self.search_vehicle_entry.get().strip()
        slots_per_level = int(os.getenv("SLOTS_PER_LEVEL"))
        for index, vehicle in enumerate(self.parking_slots):
            if vehicle and vehicle['License Plate'] == license_plate:
                vehicle_info = f"{vehicle['Level']}, Slot {(index % slots_per_level) + 1}: {vehicle['License Plate']}, Mobile: {vehicle['Mobile Number']}, Type: {vehicle['Vehicle Type']}, Level: {vehicle['Level']}"                
                messagebox.showinfo("Vehicle Found", vehicle_info)
                return
        messagebox.showerror("Error", "Vehicle not found!")

    def log_removed_vehicle(self, vehicle_info, slot_index, vehicle, entry_time, exit_time, duration, bill):
    # Define the path to the CSV file
        csv_file_path = os.path.expanduser("F:/ParkingManagement/logs/removed_vehicles.csv")

        # Check if the file exists to determine if headers need to be written
        file_exists = os.path.isfile(csv_file_path)
        
        # Determine the next serial number
        # next_serial_no = self.get_next_serial_number()
        if file_exists:
            with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)
                if len(rows) > 1:  # Check if there are any data rows
                    last_row = rows[-1]
                    next_serial_no = int(last_row[0]) + 1

        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write headers if the file is being created
            if not file_exists:
                writer.writerow(['Sr. No.', 'License Plate', 'Vehicle Type', 'Mobile Number', 'Level', 'Slot Number', 'Entry Time', 'Entry Date', 'Exit Time', 'Exit Date', 'Duration (Hours)', 'Billing', 'Employee ID'])
            
            # Write vehicle data
            writer.writerow([
                next_serial_no,  # Sr. No. is the next serial number
                vehicle['License Plate'],
                vehicle['Vehicle Type'],
                vehicle['Mobile Number'],
                vehicle['Level'],
                slot_index + 1,  # Slot Number
                entry_time.strftime("%H:%M:%S"),
                entry_time.date().strftime("%d-%m-%Y"),  # Entry Date
                exit_time.strftime("%H:%M:%S"),
                exit_time.date().strftime("%d-%m-%Y"),  # Exit Date
                vehicle_info["Duration"],
                f"Rs. {bill:.2f}",
                self.current_user_instance.get_user().get('employee_id') # Placeholder for Employee ID
            ])

    def check_parked_vehicles(self):
        current_time = datetime.now()
        notification_threshold = 6  # hours
        for index, vehicle_info in enumerate(self.parking_slots):
            if vehicle_info is not None:
                entry_time = datetime.strptime(vehicle_info["Entry Time"], "%H:%M:%S")
                entry_date = datetime.strptime(vehicle_info["Entry Date"], "%d-%m-%Y")
                entry_datetime = datetime.combine(entry_date, entry_time.time())
                duration = (current_time - entry_datetime).total_seconds() / 3600  # Convert seconds to hours        
                if duration > notification_threshold:
                    self.report_to_police(vehicle_info, index)
                    print(f"Vehicle {vehicle_info['License Plate']} standing at {vehicle_info['Level']} - Slot {index + 1} has been parked for over {notification_threshold} hours. Reported to police.")

if __name__ == "__main__":
    app.mainloop()
