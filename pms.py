# test_final.py

import customtkinter as ctk

output_filename = ""
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
        self.data_file = os.path.expanduser("F:/ParkingManagement/.data/parking_data1.json")

        
        self.title("Environment Variable Editor")

        # Creating temporary file to store the initial values
        self.temp_file_path = tempfile.mktemp()

        with open(self.temp_file_path, 'w') as temp_file:
            json.dump(self.initial_values, temp_file)

        # Widgets
        self.gst_no_label = ctk.CTkLabel(self, text="GST NO:")
        self.gst_no_label.grid(row=0, column=0, padx=10, pady=10)
        self.gst_no_entry = ctk.CTkEntry(self)
        self.gst_no_entry.grid(row=0, column=1, padx=10, pady=10)
        self.gst_no_entry.insert(0, self.initial_values['GST_NO_VAR'])

        self.smtp_server_label = ctk.CTkLabel(self, text="SMTP Server:")
        self.smtp_server_label.grid(row=1, column=0, padx=10, pady=10)
        self.smtp_server_entry = ctk.CTkEntry(self)
        self.smtp_server_entry.grid(row=1, column=1, padx=10, pady=10)
        self.smtp_server_entry.insert(0, self.initial_values['SMTP_SERVER'])

        self.smtp_port_label = ctk.CTkLabel(self, text="SMTP Port:")
        self.smtp_port_label.grid(row=2, column=0, padx=10, pady=10)
        self.smtp_port_entry = ctk.CTkEntry(self)
        self.smtp_port_entry.grid(row=2, column=1, padx=10, pady=10)
        self.smtp_port_entry.insert(0, self.initial_values['SMTP_PORT'])

        self.email_address_label = ctk.CTkLabel(self, text="Email Address:")
        self.email_address_label.grid(row=3, column=0, padx=10, pady=10)
        self.email_address_entry = ctk.CTkEntry(self)
        self.email_address_entry.grid(row=3, column=1, padx=10, pady=10)
        self.email_address_entry.insert(0, self.initial_values['PMS_EMAIL_ADDRESS'])

        self.email_password_label = ctk.CTkLabel(self, text="Email Password:")
        self.email_password_label.grid(row=4, column=0, padx=10, pady=10)
        self.email_password_entry = ctk.CTkEntry(self, show='*')
        self.email_password_entry.grid(row=4, column=1, padx=10, pady=10)
        self.email_password_entry.insert(0, self.initial_values['PMS_EMAIL_PASSWORD'])

        self.eye_button = ctk.CTkButton(
            master=self,
            text="👁️",
            command=self.toggle_password,
            width=5,
            height=20,  # To match the button's appearance with the image
        )
        self.eye_button.grid(row=4, column=2, padx=10, pady=10)

        self.num_levels_label = ctk.CTkLabel(self, text="No of Levels:")
        self.num_levels_label.grid(row=5, column=0, padx=10, pady=10)
        self.num_levels_entry = ctk.CTkEntry(self)
        self.num_levels_entry.grid(row=5, column=1, padx=10, pady=10)
        self.num_levels_entry.insert(0, self.initial_values['NUM_LEVELS'])

        self.slots_per_level_label = ctk.CTkLabel(self, text="Slots Per Level:")
        self.slots_per_level_label.grid(row=6, column=0, padx=10, pady=10)
        self.slots_per_level_entry = ctk.CTkEntry(self)
        self.slots_per_level_entry.grid(row=6, column=1, padx=10, pady=10)
        self.slots_per_level_entry.insert(0, self.initial_values['SLOT_PER_LEVEL'])

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_env_vars)
        self.save_button.grid(row=7, columnspan=2, pady=10)

        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_action)
        self.cancel_button.grid(row=8, columnspan=2, pady=10)

        self.password_visible = False

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def save_env_vars(self):
        # Get the current values from the entries
        self.current_values = {
            'GST_NO_VAR': self.gst_no_entry.get(),
            'SMTP_SERVER': self.smtp_server_entry.get(),
            'SMTP_PORT': self.smtp_port_entry.get(),
            'PMS_EMAIL_ADDRESS': self.email_address_entry.get(),
            'PMS_EMAIL_PASSWORD': self.email_password_entry.get(),
            'NUM_LEVELS': self.num_levels_entry.get(),
            'SLOT_PER_LEVEL': self.slots_per_level_entry.get()
        }

        # Extract owner information directly within this function
        try:
            with open(self.json_file_path, 'r') as file:
                data = json.load(file)

                # Search for employee data with role "Owner"
                owner_email = None
                employee_id = None
                employee_name = None

                for employee_id_key, employee_data in data.items():
                    if employee_data.get("role") == "Owner":
                        owner_email = employee_data.get('email')
                        employee_id = employee_data.get('employee_id')
                        employee_name = employee_data.get('name')
                        break  # Exit the loop after finding the owner

                if not owner_email:
                    messagebox.showerror("Error", "Owner email is missing. Please check the configuration.")
                    return

        except FileNotFoundError:
            print("The JSON file was not found.")
            messagebox.showerror("Error", "The JSON file was not found. Please check the configuration.")
            return
        except json.JSONDecodeError:
            print("Error decoding JSON. Check if the file is a valid JSON format.")
            messagebox.showerror("Error", "Error decoding JSON. Please check the file format.")
            return
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            return

        with open(self.temp_file_path, 'r') as temp_file:
            self.temp_values = json.load(temp_file)

        # Compare the initial values from the temp file with the current values
        changes_made = False
        changes = []

        # Check if the change is related to slots or levels from the temp file values
        num_levels_changed = self.current_values['NUM_LEVELS'] != self.temp_values.get('NUM_LEVELS', '')
        slots_per_level_changed = self.current_values['SLOT_PER_LEVEL'] != self.temp_values.get('SLOT_PER_LEVEL', '')

        if changes_made:
            otp = self.generate_otp()
            body_text = f"""Dear {employee_name} bearing employee ID {employee_id},

We have received a request to make changes in your confidential information. If this was not you, please change your password immediately.

Here are the changes:

{'\n'.join(changes)}

Here is your OTP: {otp}

This is an autogenerated email sent to you by the PMS system.
"""

            # Send OTP to the extracted owner email
            self.send_otp_via_email(owner_email=owner_email, otp=otp, employee_name="Owner", body_text=body_text)
            self.open_otp_verification_window()
        else:
            messagebox.showinfo("Info", "No changes made.")


    def check_vehicles_if_parked(self):
        """
        Check for vehicles parked in slots or levels beyond the updated capacity and prompt the user to remove them.
        """
        try:
            # Load initial slot and level values
            with open(self.temp_file_path, 'r') as temp_file:
                temp_data = json.load(temp_file)
                initial_slots = int(temp_data.get('SLOT_PER_LEVEL'))  # Initial slots per level from temp file
                initial_levels = int(temp_data.get('NUM_LEVELS'))  # Initial number of levels

            # Retrieve the new slot and level values from the environment
            new_slots = int(self.current_values['SLOT_PER_LEVEL'])  # New slots per level from the updated entries
            new_levels = int(self.current_values['NUM_LEVELS'])  # New number of levels

            # Check for vehicles in excess slots
            excess_vehicles_in_slots = []
            excess_vehicles_in_levels = []

            with open(self.data_file, 'r') as file:
                data = json.load(file)

                for level_data in data:
                    level = level_data.get("level")
                    slots = level_data.get("slots", [])

                    # Check if the level is beyond the new capacity
                    if level > new_levels:
                        for slot_info in slots:
                            vehicle = slot_info.get("vehicle")
                            if vehicle:  # If a vehicle is parked in a removed level
                                excess_vehicles_in_levels.append((level, slot_info.get("slot"), vehicle))

                    # Check if the slot exceeds the new capacity and has a parked vehicle
                    for slot_info in slots:
                        slot = slot_info.get("slot")
                        vehicle = slot_info.get("vehicle")
                        if slot > new_slots and vehicle:
                            excess_vehicles_in_slots.append((level, slot, vehicle))

            # Prepare messages for excess vehicles
            messages = []
            if excess_vehicles_in_slots:
                slot_message = "The following vehicles need to be removed from excess slots:\n\n"
                slot_message += "\n".join(
                    [f"Level {level}, Slot {slot}: Vehicle {vehicle}" for level, slot, vehicle in excess_vehicles_in_slots]
                )
                messages.append(slot_message)

            if excess_vehicles_in_levels:
                level_message = "The following vehicles need to be removed from excess levels:\n\n"
                level_message += "\n".join(
                    [f"Level {level}, Slot {slot}: Vehicle {vehicle}" for level, slot, vehicle in excess_vehicles_in_levels]
                )
                messages.append(level_message)

            # If there are excess vehicles, show message and cancel action
            if messages:
                complete_message = "\n\n".join(messages)
                complete_message += "\n\nPlease remove these vehicles before updating the parking configuration."
                messagebox.showinfo("Vehicles Found", complete_message)
                self.cancel_action()
                return True  # Prevent saving as there are parked vehicles in excess slots or levels

            # If no vehicles are found in excess slots or levels, proceed
            return False

        except FileNotFoundError:
            print("The JSON file was not found.")
            messagebox.showerror("Error", "The JSON file was not found. Please check the configuration.")
            return True  # Treat missing JSON file as a failure

        except json.JSONDecodeError:
            print("Error decoding JSON. Check if the file is a valid JSON format.")
            messagebox.showerror("Error", "Error decoding JSON. Please check the file format.")
            return True  # Treat JSON decoding error as a failure

        except ValueError:
            messagebox.showerror("Error", "Invalid slot or level values found. Please ensure they are integers.")
            return True  # Treat invalid values as a failure

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            return True  # Treat any other exception as a failure





    def open_otp_verification_window(self):
        self.otp_window = ctk.CTkToplevel(self)
        self.otp_window.title("OTP Verification")

        ctk.CTkLabel(self.otp_window, text="Enter OTP:").grid(row=0, column=0, padx=10, pady=10)
        otp_entry = ctk.CTkEntry(self.otp_window)
        otp_entry.grid(row=0, column=1, padx=10, pady=10)

        def verify_otp():
            if otp_entry.get() == self.otp:
                messagebox.showinfo("Success", "OTP verified. Environment variables updated successfully!")
                self.otp_window.destroy()
                self.apply_changes(self.current_values)  # Use the stored current_values
            else:
                messagebox.showerror("Error", "Invalid OTP. Please try again.")

        verify_button = ctk.CTkButton(self.otp_window, text="Verify", command=verify_otp)
        verify_button.grid(row=1, columnspan=2, pady=10)

        cancel_button = ctk.CTkButton(self.otp_window, text="Cancel", command=self.cancel_button_option)
        cancel_button.grid(row=2, columnspan=2, pady=10)

    def cancel_button_option(self):
        if hasattr(self, 'otp_window') and self.otp_window:
            self.otp_window.destroy()

    def send_otp_via_email(self, owner_email=None, otp=None, employee_name=None, body_text=None):
        # Fetch owner details if not provided
        if owner_email is None or employee_name is None:
            owner_email, employee_id, employee_name = self.extract_owner_info_from_json()

        if not owner_email:
            messagebox.showerror("Error", "Owner email not found. Please check the employee data.")
            return

        try:
            # Fetch email settings from the .env file
            sender_email = os.getenv('PMS_EMAIL_ADDRESS')
            sender_password = os.getenv('PMS_EMAIL_PASSWORD')
            smtp_server = os.getenv('SMTP_SERVER')
            smtp_port = int(os.getenv('SMTP_PORT'))

            if not sender_email or not sender_password or not smtp_server or not smtp_port:
                messagebox.showerror("Error", "Missing email configuration. Please check your .env file.")
                return

            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = owner_email
            msg['Subject'] = 'Confirm Information Change'
            msg.attach(MIMEText(body_text, 'plain'))

            # Debugging logs
            print(f"Attempting to send email:\nSMTP Server: {smtp_server}\nSMTP Port: {smtp_port}")
            print(f"Sender Email: {sender_email}\nRecipient Email: {owner_email}")

            # Establish the connection and send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, owner_email, msg.as_string())

            messagebox.showinfo("Success", "OTP sent successfully to the owner's email.")

        except smtplib.SMTPAuthenticationError as e:
            messagebox.showerror("Authentication Error", f"Failed to authenticate: {str(e)}")
        except smtplib.SMTPConnectError as e:
            messagebox.showerror("Connection Error", f"Failed to connect to the SMTP server: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def toggle_password(self):
        if self.password_visible:
            self.email_password_entry.configure(show='*')
            self.password_visible = False
        else:
            self.email_password_entry.configure(show='')
            self.password_visible = True

    def on_closing(self):
        self.destroy()


class OwnerPortal(CTk):
    def __init__(self, employee_management, employee_file_path):
        super().__init__()
        self.title("Owner Portal")
        self.geometry("450x740")
        self.employee_management = employee_management
        self.data_file = os.path.expanduser("F:/ParkingManagement/.data/parking_data.json")
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

        self.search_vehicle = CTkButton(self, text="Search Vehicle Details", command=self.open_search_window)
        self.search_vehicle.grid(row=3, column=0, padx=10, pady=(20, 5))

        self.check_vehicle = CTkButton(self, text="Check Parked Vehicle", command=self.Check_parked_veh)
        self.check_vehicle.grid(row=4, column=0, padx=10, pady=(20, 5))

        self.add_blacklist_vehicle_button = CTkButton(self, text="Add to Blacklisted Vehicle", command=self.add_blacklist_vehicle)
        self.add_blacklist_vehicle_button.grid(row=5, column=0, padx=10, pady=(20, 5))

        self.rem_blacklist_vehicle_button = CTkButton(self, text="Remove from Blacklisted Vehicle", command=self.rem_blacklist_vehicle)
        self.rem_blacklist_vehicle_button.grid(row=6, column=0, padx=10, pady=(20, 5))

        self.change_password_button = CTkButton(self, text="Change Employee Password", command=self.change_password)
        self.change_password_button.grid(row=7, column=0, padx=10, pady=(20, 5))

        self.change_details_button = CTkButton(self, text="Change Employee Details", command=self.change_details)
        self.change_details_button.grid(row=8, column=0, padx=10, pady=(20, 5))

        self.check_vehicle_records_button = CTkButton(self, text="Check Vehicle Records", command=self.check_vehicle_records)
        self.check_vehicle_records_button.grid(row=9, column=0, padx=10, pady=(20, 5))

        self.check_employee_records_button = CTkButton(self, text="Check Employee Records", command=self.check_employee_records)
        self.check_employee_records_button.grid(row=10, column=0, padx=10, pady=(20, 5))

        self.check_employee_details_changes = CTkButton(self, text="Check Changes in Employee Details", command=self.emp_details_changes)
        self.check_employee_details_changes.grid(row=11, column=0, padx=10, pady=(20, 5))

        self.change_confidential_info = CTkButton(self, text="Change Confidential Information", command=self.change_confidential_information)
        self.change_confidential_info.grid(row=12, column=0, padx=10, pady=(20, 5))

        self.logout_button = CTkButton(self, text="Logout", command=self.on_logout)
        self.logout_button.grid(row=13, column=0, padx=10, pady=(20, 5))

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


    def on_logout(self):
        self.destroy()
        login_window = LoginWindow(self.employee_management)
        login_window.mainloop()


    def change_details(self):
        UpdateEmployeeDetails(self.employee_management)

    def show_employees(self):
        EmployeeDetailsView(self.employee_file_path).mainloop()

    def open_search_window(self):
        """Open a new window to search for a vehicle."""
        search_window = ctk.CTkToplevel(self)
        search_window.title("Search Vehicle")
        search_window.geometry("400x150")

        # Add search UI elements to the new window
        ctk.CTkLabel(search_window, text="Search Vehicle:").grid(row=0, column=0, padx=10, pady=5)
        search_vehicle_entry = ctk.CTkEntry(search_window, width=200, placeholder_text="Enter License Plate")
        search_vehicle_entry.grid(row=0, column=1, padx=10, pady=5)

        def cancel_search():
            search_window.destroy()  # Close the search window

        def search_vehicle():
            """Search for a vehicle by license plate."""
            license_plate = search_vehicle_entry.get().strip()

            # Load parked vehicles from parking_data.json
            try:
                with open(self.data_file, 'r') as file:
                    parked_vehicles = json.load(file)
                    for vehicle in parked_vehicles:
                        if vehicle["License Plate"] == license_plate:
                            vehicle_info = (
                                f"License Plate: {vehicle['License Plate']}\n"
                                f"Mobile Number: {vehicle['Mobile Number']}\n"
                                f"Vehicle Type: {vehicle['Vehicle Type']}\n"
                                f"Level: {vehicle['Level']}\n"
                                f"Slot: {vehicle['Slot']}\n"
                                f"Entry Date: {vehicle['Entry Date']}\n"
                                f"Entry Time: {vehicle['Entry Time']}"
                            )
                            messagebox.showinfo("Vehicle Found", vehicle_info)
                            return

                messagebox.showerror("Error", "Vehicle not found!")
            except Exception as e:
                messagebox.showerror("Error", f"Error searching vehicle: {str(e)}")

        # Search button in the new window
        ctk.CTkButton(search_window, text="Search", command=search_vehicle).grid(row=1, column=1, padx=10, pady=5)
        ctk.CTkButton(search_window, text="Cancel", command=cancel_search).grid(row=2, column=1, padx=10, pady=5)


    def Check_parked_veh(self):
        pms = ParkingManagementSystem(self.employee_management)
        pms.show_parked_vehicles()

    def add_blacklist_vehicle(self):
        blacklist_file_path = os.path.expanduser("F:/ParkingManagement/.data/blacklisted_vehicle.json")
        bl = BlacklistVehicleApp(blacklist_file_path)
        bl.mainloop()

    def rem_blacklist_vehicle(self):
        blacklist_file_path = os.path.expanduser("F:/ParkingManagement/.data/blacklisted_vehicle.json")
        rbl = RemoveBlacklistedVehicleApp(blacklist_file_path)
        rbl.mainloop()

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
            text="👀",
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

        self.verify_otp_button = ctk.CTkButton(
            self.changepassword, 
            text="Verify OTP", 
            command=self.verify_otp, 
            state="disabled"  # Initial state is disabled
            )
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

        if employee_id == "Select Employee":
            messagebox.showerror("Error", "Please select a valid employee ID.")
            return

        if not new_password:
            messagebox.showerror("Error", "Please enter a new password.")
            return

        if employee_id in self.users:
            email = self.users[employee_id]['email']
            if email:
                # Generate and send OTP
                otp = self.generate_otp()  # Assuming you have this method
                self.users[employee_id]['otp'] = otp  # Temporarily store OTP in memory
                self.users[employee_id]['new_password'] = new_password
                self.send_otp_via_email(email, otp, self.users[employee_id]['name'], self.current_user_instance.get_user()['role'], self.current_user_instance.get_user()['name'])
                messagebox.showinfo("OTP Sent", "An OTP has been sent to the registered email.")
    
                # Enable the "Verify OTP" button
                self.verify_otp_button.configure(state="normal")
            else:
                messagebox.showerror("Error", "No email found for the employee.")
        else:
            messagebox.showerror("Error", "Employee ID not found.")

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

    def generate_otp(self):
        """Generate a 6-digit random OTP."""
        return str(random.randint(100000, 999999))


    def verify_otp(self):
        employee_id = self.employee_id_dropdown.get()
        otp = self.otp_entry.get()

        if employee_id in self.users and self.users[employee_id].get('otp') == otp:
            # Update password
            self.users[employee_id]['password'] = self.users[employee_id]['new_password']
            del self.users[employee_id]['new_password']  # Remove temporary new_password
            del self.users[employee_id]['otp']  # Remove OTP to avoid saving it

            # Save the updated password to the JSON file
            self.save_users_to_json(self.users)
            
            messagebox.showinfo("Success", "Password updated successfully.")
            self.back_button_cancel()  # Close the change password window

            # Disable the "Verify OTP" button again
            self.verify_otp_button.configure(state="disabled")
        else:
            messagebox.showerror("Error", "Invalid OTP.")


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
        self.update_employee_ages()

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

    def update_employee_ages(self):
        """Update the age of all employees based on their date of birth."""
        for employee_id, details in self.users.items():
            if "Date of Birth" in details:
                dob_str = details["Date of Birth"]
                try:
                    # Parse the stored date of birth string
                    day, month, year = dob_str.split()
                    month_dict = {
                        "January": 1, "February": 2, "March": 3, "April": 4,
                        "May": 5, "June": 6, "July": 7, "August": 8,
                        "September": 9, "October": 10, "November": 11, "December": 12
                    }
                    month_number = month_dict[month]
                    dob = date(int(year), month_number, int(day))
                    
                    # Update age in the user dictionary
                    age = self.calculate_age(dob)
                    self.users[employee_id]["age"] = age
                except Exception as e:
                    print(f"Error updating age for Employee ID {employee_id}: {e}")

        # Save updated users to the JSON file
        self.save_user_data()

    def calculate_age(self, dob):
        """Calculate the age based on the date of birth."""
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age


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

        self.credits_box = ctk.CTkButton(self, text="Credits", command=self.show_credits)
        self.credits_box.grid(row=8, column=1, columnspan=2, padx=10, pady=5)

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
        elif role == "Co-Owner":
            self.destroy()
            # CoOwnerPortal(self.employee_management).mainloop()
        elif role == "Manager":
            self.destroy()
            # ManagerPortal(self.employee_management).mainloop()
        elif role == "Employee":
            self.destroy()
            ParkingManagementSystem(self.employee_management).mainloop()
        else:
            print("Unauthorized access attempt.")

    def show_credits(self):
        credits_text = """
        Credits:

        Developer: Team Eagle
        Project: Parking Management System
        Tools & Libraries:
        - Python 3.x
        - Tkinter (CustomTkinter)
        - smtplib
        - os, json
        - More...
        """
        
        messagebox.showinfo("Credits", credits_text)


class CustomLoadingAnimation:
    def __init__(self, employee_management):
        self.employee_management = employee_management
        self.screen = turtle.Screen()
        self.screen.bgcolor("black")
        self.screen.setup(width=500, height=400)
        self.screen.title("V-Park Parkings")

        self.pen = turtle.Turtle()
        colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet", "white"]
        self.pen.color(random.choice(colors))
        self.pen.speed(3)

        self.total_time = random.uniform(3, 8)
        self.num_characters = len("V -Park Parkings") 
        self.delay = self.total_time / self.num_characters

    def write_text(self, text, position, font):
        self.pen.penup()
        self.pen.goto(position)
        self.pen.pendown()
        for char in text:
            self.pen.write(char, font=font)
            time.sleep(self.delay)  
            self.pen.penup()
            if char != " ":
                # Adjust spacing based on character width
                if char in "ilIj.,:;'\"": # narrow characters
                    self.pen.forward(20)
                elif char in "mwWMQgkV": # wide characters
                    self.pen.forward(35)
                else: # medium width characters
                    self.pen.forward(25)
            else:
                self.pen.forward(15)  # Space between words
            self.pen.pendown()

    def display_text(self):
        # First text
        self.pen.clear()  # Clear any previous drawings
        self.write_text("V-Park", position=(-150, 0), font=("Bradley Hand ITC", 36, "bold"))
        
        # Pause between animations
        time.sleep(1)
        
        # Add second text (without clearing first)
        self.write_text("Parkings", position=(-150, -50), font=("Bradley Hand ITC", 36, "bold"))
        
        self.pen.hideturtle()
        time.sleep(2)
        self.screen.bye()


class ParkingManager:
    def __init__(self):
        self.data_file = os.path.expanduser("F:/ParkingManagement/.data/parking_data1.json")
        self.data_file_2 = os.path.expanduser("F:/ParkingManagement/.data/parking_data.json")
        self.dotenv_path = os.path.expanduser("F:/ParkingManagement/.data/.env")
        if os.path.exists(self.dotenv_path):
            load_dotenv(self.dotenv_path)
        else:
            print(f".env file does not exist at path: {self.dotenv_path}")
        self.env_last_modified = None
        self.parking_data = None

        # Load environment variables and initialize parking data
        self.load_env_variables()
        self.parking_data = self.load_parking_data()
        self.rebuild_parking_structure()

    def load_env_variables(self):
        """ Load environment variables from the .env file. """
        load_dotenv(self.dotenv_path)
        try:
            self.num_levels = int(os.getenv("NUM_LEVELS"))  # Default to 5 levels
            self.slots_per_level = int(os.getenv("SLOT_PER_LEVEL"))  # Default to 10 slots per level
            print(f"Environment Variables Loaded: NUM_LEVELS={self.num_levels}, SLOT_PER_LEVEL={self.slots_per_level}")
        except ValueError as e:
            print("Error parsing environment variables:", str(e))
            raise

    def load_parking_data(self):
        """ Load parking data from the JSON file. Initialize if not found or invalid. """
        try:
            with open(self.data_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Parking data not found or invalid. Initializing...")
            return self.initialize_parking_data()

    def save_parking_data(self, data=None):
        """ Save parking data to the JSON file with safety measures. """
        if not data:
            data = self.parking_data
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

        temp_file = self.data_file + ".temp"
        with open(temp_file, "w") as file:
            json.dump(data, file, indent=4)

        # Replace original file only after successful write
        os.replace(temp_file, self.data_file)
        print("Parking data safely updated.")

    def rebuild_parking_structure(self):
        """ Rebuild parking structure according to the environment variables, ensuring no data loss. """
        try:
            # Load current data
            parking_data = self.load_parking_data()
            
            # Ensure the parking structure matches the number of levels and slots per level as per the .env configuration
            updated_parking_data = []
            for i in range(self.num_levels):
                level = parking_data[i] if i < len(parking_data) else {"level": i + 1, "slots": []}
                current_slots = len(level["slots"])

                # Add or remove slots as needed
                if current_slots < self.slots_per_level:
                    for j in range(self.slots_per_level - current_slots):
                        level["slots"].append({"slot": current_slots + j + 1, "vehicle": None})
                elif current_slots > self.slots_per_level:
                    level["slots"] = level["slots"][:self.slots_per_level]  # Trim to the correct number of slots

                updated_parking_data.append(level)

            # Save the updated structure back to the file
            self.save_parking_data(updated_parking_data)
            print("Parking structure rebuilt successfully.")

        except Exception as e:
            print(f"Error while rebuilding parking structure: {e}")

    def remove_slots_from_parking_data(self, parking_data, slots_to_remove):
        """ Remove slots from parking_data to balance with the other file. """
        for level in parking_data:
            while slots_to_remove > 0 and level["slots"]:
                level["slots"].pop()  # Remove the last slot
                slots_to_remove -= 1
        self.save_parking_data(parking_data)

    def remove_slots(self, level_number, slots_to_remove):
        """
        Remove slots from a specific level.
        """
        for level in self.parking_data:
            if level["level"] == level_number:
                if slots_to_remove > len(level["slots"]):
                    return "Cannot remove more slots than available."
                level["slots"] = level["slots"][:-slots_to_remove]
                self.save_parking_data()
                return f"Removed {slots_to_remove} slots from Level {level_number}."
        return "Level not found."

    def add_slots(self, level_number, additional_slots):
        """
        Add slots to a specific level.
        """
        for level in self.parking_data:
            if level["level"] == level_number:
                current_slots = len(level["slots"])
                new_slots = [{"slot": i + 1, "vehicle": None} for i in range(current_slots, current_slots + additional_slots)]
                level["slots"].extend(new_slots)
                self.save_parking_data()
                return f"Added {additional_slots} slots to Level {level_number}."
        return "Level not found."

    
class ParkingManagementSystem(ctk.CTk):
    def __init__(self, employee_management):
        super().__init__()

        self.title("Parking Management System")
        self.geometry("600x500")
        self.employee_management = employee_management
        self.after_id = None
        self.current_user_instance = CurrentUser.get_instance()
        file_path = os.path.expanduser("F:/ParkingManagement/.data/parking_data.json")
        self.num_levels = int(os.getenv('NUM_LEVELS'))
        self.slots_per_level = int(os.getenv('SLOT_PER_LEVEL'))
        self.parking_slots = [None] * (self.num_levels * self.slots_per_level)
        self.vehicle_window = None
        self.parked_vehicles = {}
        self.data_file = file_path  # JSON file to store parking data
        self.load_parking_data()
        self.update_slots_per_level()
        self.parking_manager = ParkingManager()
        self.parking_manager.rebuild_parking_structure()
        self.parking_data = []
        self.backup_file = self.data_file + ".backup"

        # self.schedule_vehicle_checks()

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as file:
                json.dump(self.parking_slots, file, indent=4, default=str)
            print(f"Created new JSON file at: {file_path}")
        else:
            print(f"JSON file already exists at: {file_path}")

        self.parking_data1_file = os.path.expanduser("F:/ParkingManagement/.data/parking_data1.json")
        os.makedirs(os.path.dirname(self.parking_data1_file), exist_ok=True)
        if not os.path.isfile(self.parking_data1_file):
            with open(self.parking_data1_file, 'w') as file:
                json.dump([], file, indent=4)  # Initialize with an empty list
            print(f"Created new JSON file at: {self.parking_data1_file}")
        else:
            print(f"JSON file already exists at: {self.parking_data1_file}")

        # License Plate Entry
        ctk.CTkLabel(self, text="License Plate:").grid(row=0, column=0, padx=10, pady=(20, 5))
        self.license_plate_entry = ctk.CTkEntry(self, width=200, placeholder_text="Enter License Plate")
        self.license_plate_entry.grid(row=0, column=1, padx=10, pady=(20, 5))

        # Mobile Number Entry
        ctk.CTkLabel(self, text="Mobile Number:").grid(row=1, column=0, padx=10, pady=5)
        self.mobile_number_entry = ctk.CTkEntry(self, width=200, placeholder_text="Enter Mobile Number")
        self.mobile_number_entry.grid(row=1, column=1, padx=10, pady=5)

        # Vehicle Type
        ctk.CTkLabel(self, text="Vehicle Type:").grid(row=2, column=0, padx=10, pady=5)
        vehicle_list = ["Select Vehicle", "2-wheeler", "Car", "Jeep", "Taxi", "Pickup-truck", "Army", "Ambulance", "Police", "Other 4-wheeler"]
        self.vehicle_type = ctk.CTkOptionMenu(self, values=vehicle_list)
        self.vehicle_type.set(vehicle_list[2])
        self.vehicle_type.grid(row=2, column=1, padx=10, pady=5)

        # Parking Level
        ctk.CTkLabel(self, text="Parking Level:").grid(row=3, column=0, padx=10, pady=5)
        levels = ["Select Level", "Level 1", "Level 2", "Level 3", "Level 4"]
        self.level_number = ctk.CTkOptionMenu(self, values=levels)
        self.level_number.set(levels[1])
        self.level_number.grid(row=3, column=1, padx=10, pady=5)

        # Buttons
        ctk.CTkButton(self, text="Park Vehicle", command=self.park_vehicle).grid(row=4, column=1, padx=10, pady=5)
        ctk.CTkButton(self, text="Remove Vehicle", command=self.remove_vehicle).grid(row=5, column=1, padx=10, pady=5)
        ctk.CTkButton(self, text="Show Parked Vehicles", command=self.show_parked_vehicles).grid(row=6, column=1, padx=10, pady=5)

        # Search Vehicle
        ctk.CTkLabel(self, text="Search Vehicle:").grid(row=7, column=0, padx=10, pady=5)
        self.search_vehicle_entry = ctk.CTkEntry(self, width=200, placeholder_text="Enter License Plate")
        self.search_vehicle_entry.grid(row=7, column=1, padx=10, pady=5)
        ctk.CTkButton(self, text="Search", command=self.search_vehicle).grid(row=7, column=2, padx=10, pady=5)

        # Log Out Button
        ctk.CTkButton(self, text="Log Out", command=self.on_logout).grid(row=8, column=1, padx=10, pady=5)

        # QR Scan Button
        ctk.CTkButton(self, text="Scan QR Code", command=self.scan_qr_code).grid(row=9, column=1, padx=10, pady=5)

    def on_logout(self):
        try:
            # Before logging out, ensure data is saved
            self.save_parking_data()
            self.upload_parking_data()
            # Perform any other logout actions (like clearing session or resetting the UI)
            messagebox.showinfo("Logout", "Successfully logged out.")
            self.destroy()  # This will close the application if needed
            login_window = LoginWindow(self.employee_management)
            login_window.mainloop()
        except Exception as e:
            print(f"Error during logout: {e}")
            messagebox.showerror("Error", f"Error during logout: {e}")

    def load_parking_data(self):
        try:
            with open(self.data_file, 'r') as file:
                self.parking_slots = json.load(file)
                print(f"Loaded parking data from: {self.data_file}")
        except (FileNotFoundError, json.JSONDecodeError):
            self.parking_slots = [None] * (self.num_levels * self.slots_per_level)

    def save_parking_data(self, vehicle_info=None):
        if not vehicle_info:
            print("No vehicle information to save. Skipping save operation.")
            return  

        try:
            # Save the current parking slots to the .json file
            with open(self.data_file, 'a') as file:
                json.dump(vehicle_info, file, indent=4, default=str)
            print("Parking data saved successfully.")

            self.upload_parking_data()

        except Exception as e:
            print(f"Error saving parking data: {e}")
            messagebox.showerror("Error", f"Error saving parking data: {e}")

    def upload_parking_data(self):
        """Upload the parking data to the Flask server with a waiting dialog."""
        try:
            with open(self.parking_data1_file, 'rb') as file:
                files = {'json_file': (os.path.basename(self.parking_data1_file), file, 'application/json')}
                url = 'https://gaba1.pythonanywhere.com/upload_parking_data'

                # Perform upload
                response = requests.post(url, files=files)

                print(f"Server Response: {response.text}")

                if response.status_code == 200:
                    print("Parking data uploaded successfully.")
                    # messagebox.showinfo("Success", "Parking data uploaded successfully!")
                else:
                    print(f"Failed to upload parking data: {response.status_code}")
                    messagebox.showerror("Error", f"Failed to upload parking data: {response.status_code}")

                # Parse JSON response
                try:
                    response_json = response.json()
                    print(response_json)
                except ValueError:
                    print("Invalid JSON response from the server.")
                    messagebox.showerror("Error", "Server returned an invalid response.")
        except Exception as e:
            print(f"Error uploading parking data: {e}")
            messagebox.showerror("Error", f"Error uploading parking data: {e}")

    def start_upload(self):
        """Start the upload process in a separate thread."""
        threading.Thread(target=self.upload_parking_data, daemon=True).start()

    def scan_qr_code(self):
        def update_frame():
            """Capture frame and update tkinter window."""
            ret, frame = cap.read()
            if ret:
                decoded_objects = decode(frame)
                for obj in decoded_objects:
                    qr_data = obj.data.decode('utf-8')
                    try:
                        license_plate, mobile_number, vehicle_type = self.extract_qr_data(qr_data)
                        self.notify_attendant(license_plate, mobile_number, vehicle_type)
                    except ValueError:
                        messagebox.showerror("Error", "QR code data is not in the correct format.")
                
                # Convert frame to ImageTk
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                camera_label.imgtk = imgtk
                camera_label.configure(image=imgtk)

            if running:
                camera_label.after(10, update_frame)
            else:
                cap.release()
                cv2.destroyAllWindows()

        def stop_scanning():
            """Stop the camera and close the tkinter window."""
            nonlocal running
            running = False
            scanner_window.destroy()

        # Initialize a new customtkinter window for scanning
        scanner_window = ctk.CTkToplevel(self)
        scanner_window.title("QR Code Scanner")
        scanner_window.geometry("575x475")  # Adjust as needed

        # Start capturing video
        cap = cv2.VideoCapture(0)
        running = True

        # Camera feed display label
        camera_label = ctk.CTkLabel(scanner_window, text="")
        camera_label.pack(pady=20)

        # Close button
        stop_button = ctk.CTkButton(scanner_window, text="Stop Scanning", command=stop_scanning, fg_color="red", text_color="white")
        stop_button.pack(pady=10)

        # Start updating frames
        update_frame()

    
    def notify_attendant(self, license_plate, mobile_number, vehicle_type):
        # Display notification with options for vehicle action
        response = messagebox.askquestion(
            "Vehicle Action Required",
            f"License Plate: {license_plate}\n"
            f"Mobile Number: {mobile_number}\n"
            f"Vehicle Type: {vehicle_type}\n\n"
            "Would you like to park or remove the vehicle?",
            icon='question'
        )

        if response == 'yes':
            if self.is_vehicle_parked(license_plate):
                self.remove_vehicle(license_plate)
                messagebox.showinfo("Success", f"Vehicle {license_plate} removed successfully.")
            else:
                messagebox.showinfo("Success", f"Vehicle {license_plate} parked successfully.")
        else:
            messagebox.showinfo("Cancelled", "Operation cancelled by the attendant.")
    
    def is_vehicle_parked(self, license_plate):
        # Check if the vehicle is already parked in JSON data
        for slot in self.parking_slots:
            if slot and slot.get("License Plate") == license_plate:
                return True
        return False

    def park_vehicle(self):
        try:
            # Assign level based on vehicle type
            if vehicle_type.lower() == "2-wheeler":
                level = 4
            else:
                try:
                    level = int(self.level_number.get().split()[1])  # Extract level number
                    if level == 4:
                        messagebox.showerror("Error", "Level 4 is reserved for 2-wheelers only.")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Invalid level selected.")
                    return

            # Regular expression for validating license plate format
            normalize_license_plate = (
                r'^[A-Z]{2}\d{2}[A-Z]{1}\d{4}$|^[A-Z]{2}\d{1}[A-Z]{3}\d{4}$|'  # PB12PP1234 or PB13P1234
                r'^[A-Z]{2}\d{1}[A-Z]{2}\d{4}$|^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$|'  # DL1CA1234 or DL1CAB1234
                r'^\d{2}[A-Z]{1}\d{6}[A-Z]{1}$|^\d{2}[B]{1}[H]{1}\d{4}[A-Z]{2}$|^\d{2}[B]{1}[H]{1}\d{4}[A-Z]{1}$'  # 11A123456A or 24BH1234PP or 24BH1234P
            )

            # Validate inputs
            if not re.match(normalize_license_plate, license_plate):
                messagebox.showerror("Error", "Invalid license plate format.")
                return

            if not re.match(r'^\d{10}$', mobile_number):
                messagebox.showerror("Error", "Invalid mobile number. Must be 10 digits.")
                return

            blacklist_file_path = os.path.expanduser("F:/ParkingManagement/.data/blacklisted_vehicle.json")
            with open(blacklist_file_path, 'r') as blacklist_file:
                blacklist_data = json.load(blacklist_file)

            # Check if the vehicle is blacklisted
            blacklisted_vehicle = next(
                (entry for entry in blacklist_data if entry["License Plate"] == license_plate), None
            )
            if blacklisted_vehicle:
                messagebox.showerror(
                    "Blacklisted Vehicle",
                    f"Vehicle {license_plate} is blacklisted.\nReason: {blacklisted_vehicle['Reason']}"
                )
                return

            with open(self.parking_data1_file, 'r+') as file:
                data = json.load(file)  # Load parking data

                # Find the Selected Level
                level_entry = next((lvl for lvl in data if lvl["level"] == level), None)

                if level_entry is None:
                    messagebox.showerror("Error", f"Level {level} does not exist.")
                    return

                # Find the First Available Slot in the Selected Level
                for slot in level_entry["slots"]:
                    if slot.get("vehicle") is None:  # Check if slot is vacant
                        entry_date = datetime.now().strftime("%d-%m-%Y")
                        entry_time = datetime.now().strftime("%H:%M:%S")

                        # Assign the slot
                        slot["vehicle"] = {
                            "License Plate": license_plate,
                            "Vehicle Type": vehicle_type,
                            "Entry Date": entry_date,
                            "Entry Time": entry_time
                        }

                        # Save Updated Data
                        file.seek(0)
                        json.dump(data, file, indent=4)
                        file.truncate()

                        # Show Success Message
                        messagebox.showinfo("Success", f"Vehicle parked successfully in Level {level}, Slot {slot['slot']}.")

                        self.upload_parking_data()
                        self.add_to_parking_data2(vehicle_info)

                        # Clear the fields on the GUI
                        self.clear_fields()

                        # Send WhatsApp notification
                        phone_no = "+91" + str(mobile_number)
                        message = (
                            f"\u26A0\uFE0FParking Alert!\u26A0\uFE0F\nYour vehicle has been successfully parked \ud83d\ude97\n"
                            f"{license_plate}\n{vehicle_type}\nLevel {level}\n"
                            f"Slot {slot['slot']}.\nEntry Time: {entry_time}\nEntry Date: {entry_date}\n"
                            f"At \ud83d\udc49 V-Park Parkings"
                        )
                        self.send_whatsapp_message(phone_no, message)
                        return

                # If no available slot is found
                messagebox.showerror("Error", f"No available parking slots in Level {level}.")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def clear_fields(self):
        # Clear the input fields
        self.license_plate_entry.delete(0, 'end')
        self.mobile_number_entry.delete(0, 'end')
        self.vehicle_type.set("Select Vehicle")
        self.level_number.set("Select Level")


    def add_to_parking_data2(self, vehicle_info):
        try:
            # Load existing data (if any)
            existing_data = []
            with open(self.data_file, 'r') as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    pass  # Ignore empty file

            # Create a complete list of parked vehicles
            parked_vehicles = []
            for entry in existing_data:
                if entry:
                    parked_vehicles.append(entry)

            # Add the new vehicle information
            parked_vehicles.append(vehicle_info)

            # Write the complete list to the file
            with open(self.data_file, 'w') as file:
                json.dump(parked_vehicles, file, indent=4)

        except Exception as e:
            print(f"Error saving to {self.data_file}: {e}")
            messagebox.showerror("Error", f"Error saving vehicle info: {e}")

    def send_whatsapp_message(self, phone_no, message):
            client = Client(account_sid, auth_token)

            clean_message = message.encode("utf-8", "ignore").decode("utf-8")

            # Send WhatsApp message
            message_response = client.messages.create(
                from_=twilio_whatsapp_number,
                body=clean_message,
                to=f"whatsapp:{phone_no}"
            )
            
            print(f"WhatsApp message sent successfully to {phone_no}")
            print(f"Message SID: {message_response.sid}")
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")



    # def send_whatsapp_message(self, phone_no, message):
    #     # Get current time
    #     now = datetime.now()
    #     current_hour = now.hour
    #     current_minute = now.minute

    #     # Add 1 minute to the current time
    #     future_minute = current_minute + 1
    #     future_hour = current_hour

    #     # Handle minute overflow
    #     if future_minute >= 60:
    #         future_minute -= 60
    #         future_hour += 1

    #     # Handle hour overflow (optional, depending on the library's requirements)
    #     if future_hour >= 24:
    #         future_hour -= 24

    #     # Open WhatsApp Web and send the message
    #     kit.sendwhatmsg(phone_no, message, future_hour, future_minute)
    
    #     # Wait for WhatsApp Web to open
    #     time.sleep(5)
        
    #     # Send the message
    #     pyautogui.press('enter')

    #     time.sleep(5)
        
    #     # Close the browser window (assuming the browser is the active window)
    #     pyautogui.hotkey('ctrl', 'w')

    # def send_whatsapp_document(self, phone_no, output_filename, message):
    #     try:
    #         # Open WhatsApp Web for the specified phone number
    #         # phone_no = "+91" + vehicle['Mobile Number']
    #         webbrowser.open(f"https://web.whatsapp.com/send?phone={phone_no}")
    #         time.sleep(20)  # Wait for WhatsApp Web to load

    #         # Debug statement to ensure file exists
    #         plus_sign_image_path = os.path.expanduser("F:/ParkingManagement/requirements/plus_sign.png")
    #         if not os.path.isfile(plus_sign_image_path):
    #             raise FileNotFoundError(f"{plus_sign_image_path} not found.")

    #         # Locate the plus sign icon and click it
    #         plus_sign_btn = pyautogui.locateCenterOnScreen(plus_sign_image_path, confidence=0.9)
    #         if plus_sign_btn:
    #             pyautogui.click(plus_sign_btn)
    #             time.sleep(2)
                
    #             # Locate the document icon and click it
    #             document_image_path = os.path.expanduser("F:/ParkingManagement/requirements/document_button.png")
    #             if not os.path.isfile(document_image_path):
    #                 raise FileNotFoundError(f"{document_image_path} not found.")
    #             document_btn = pyautogui.locateCenterOnScreen(document_image_path, confidence=0.9)
    #             if document_btn:
    #                 pyautogui.click(document_btn)
    #                 time.sleep(2)
                    
    #                 # Type the absolute path of the document and press enter
    #                 pyautogui.write(os.path.abspath(output_filename))
    #                 pyautogui.press('enter')
    #                 time.sleep(3)

    #                 # Locate the send button and click it
    #                 send_image_path = os.path.expanduser("F:/ParkingManagement/requirements/send_button.png")
    #                 if not os.path.isfile(send_image_path):
    #                     raise FileNotFoundError(f"{send_image_path} not found.")
    #                 send_btn = pyautogui.locateCenterOnScreen(send_image_path, confidence=0.9)

    #                 pyautogui.press('enter')
                    
    #                 if send_btn:
    #                     pyautogui.click(send_btn)
    #                     time.sleep(7)
    #                 else:
    #                     pyautogui.press('enter')
    #                     print("Send button not found.")
    #             else:
    #                 print("Document button not found.")
    #         else:
    #             print("Plus sign button not found.")
    #         pyautogui.hotkey('ctrl', 'w')
    #     except Exception as e:
    #         print(f"An error occurred: {e}")


    def calculate_duration(self, entry_time, exit_time):
        duration = exit_time - entry_time
        total_seconds = duration.total_seconds()
        total_hours = int(total_seconds // 3600)  # Convert seconds to hours
        minutes = int((total_seconds % 3600) // 60)  # Remaining minutes
        seconds = int(total_seconds % 60)  # Remaining seconds
        
        return total_hours, minutes, seconds

    def remove_vehicle(self, license_plate=None):
        if not license_plate:
            license_plate = self.license_plate_entry.get()

        found = False
        exit_time_o = datetime.now()
        exit_time_w = exit_time_o.time().strftime("%H:%M:%S")
        exit_date = exit_time_o.date().strftime("%d-%m-%Y")

        try:
            # Open the parking_data1.json file
            with open(self.parking_data1_file, 'r+') as parking_file:
                parking_data1 = json.load(parking_file)

                for level in parking_data1:
                    for slot in level["slots"]:
                        vehicle = slot.get("vehicle")  # Retrieve the vehicle data
                        if vehicle and vehicle["License Plate"] == license_plate:
                            found = True

                            # Load data from parking_data.json
                            with open(self.data_file, 'r') as data_file:
                                parked_vehicles = json.load(data_file)

                            # Find the vehicle in the main record
                            vehicle_info = next((v for v in parked_vehicles if v["License Plate"] == license_plate), None)
                            if vehicle_info is None:
                                messagebox.showerror("Error", "Vehicle not found in parking_data.json!")
                                return

                            # Calculate parking duration and billing
                            entry_time = datetime.strptime(
                                f"{vehicle_info['Entry Date']} {vehicle_info['Entry Time']}", "%d-%m-%Y %H:%M:%S"
                            )
                            exit_time = datetime.strptime(
                                f"{exit_date} {exit_time_w}", "%d-%m-%Y %H:%M:%S"
                            )
                            bill_without_gst, cgst, sgst = self.calculate_billing(total_hours, vehicle_info['Vehicle Type'])
                            total_bill = bill_without_gst + cgst + sgst

                            # Prepare receipt details
                            receipt_data = {
                                "License Plate": license_plate,
                                "Vehicle Type": vehicle_info['Vehicle Type'],
                                "Mobile Number": vehicle_info['Mobile Number'],
                                "Level": level["level"],
                                "Slot": slot["slot"],
                                "Entry Date": vehicle_info['Entry Date'],
                                "Entry Time": vehicle_info['Entry Time'],
                                "Exit Date": exit_date,
                                "Exit Time": exit_time_w,
                                "Duration": time_stayed,
                                "Cost": bill_without_gst,
                                "CGST": cgst,
                                "SGST": sgst,
                                "Total Cost": total_bill
                            }

                            # Remove the vehicle from parking_data1.json
                            slot["vehicle"] = None
                            parking_file.seek(0)
                            json.dump(parking_data1, parking_file, indent=4)
                            parking_file.truncate()

                            # Remove the vehicle from parking_data.json
                            with open(self.data_file, 'r+') as data_file:
                                parked_vehicles = [v for v in parked_vehicles if v["License Plate"] != license_plate]
                                data_file.seek(0)
                                json.dump(parked_vehicles, data_file, indent=4)
                                data_file.truncate()

                            # Send WhatsApp notification with receipt
                            self.send_whatsapp_bill(mob_no, receipt_data)

                            # Show the bill amount
                            messagebox.showinfo("Bill", f"Total bill for {license_plate} is: ₹{total_bill:.2f}")
                            return

            # If the vehicle was not found in any slot
            if not found:
                messagebox.showerror("Error", "Vehicle not found in parking records!")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def calculate_billing(self, hours, vehicle_type):
        
        exempt_vehicles = ["Army", "Police"]
        if any(keyword in vehicle_type for keyword in exempt_vehicles):
            return 0, 0, 0
        
        elif vehicle_type in ["Ambulance"]:
            return 0, 0, 0
        
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

    def send_whatsapp_bill(self, phone_no, vehicle_info):
        try:

            # Formatting bill message
            message = (
                f"\u2705 Parking Bill \u2705\n"
                f"License Plate: {vehicle_info['License Plate']}\n"
                f"Vehicle Type: {vehicle_info['Vehicle Type']}\n"
                f"Mobile Number: {vehicle_info['Mobile Number']}\n"
                f"Level: {vehicle_info['Level']}\n"
                f"Slot: {vehicle_info['Slot']}\n"
                f"Entry Date: {vehicle_info['Entry Date']}\n"
                f"Entry Time: {vehicle_info['Entry Time']}\n"
                f"Exit Date: {vehicle_info['Exit Date']}\n"
                f"Exit Time: {vehicle_info['Exit Time']}\n"
                f"Duration: {vehicle_info['Duration'][0]} hrs {vehicle_info['Duration'][1]} min {vehicle_info['Duration'][2]} sec\n"
                f"Cost: ₹{vehicle_info['Cost']:.2f}\n"
                f"CGST: ₹{vehicle_info['CGST']:.2f}\n"
                f"SGST: ₹{vehicle_info['SGST']:.2f}\n"
                f"Total Cost: ₹{vehicle_info['Total Cost']:.2f}\n"
                f"\u2728 Thank you for using V-Park Parkings! \u2728"
            )

            client.messages.create(
                from_=twilio_whatsapp_number,
                body=message,
                to=f"whatsapp:{phone_no}"
            )
            
            print(f"WhatsApp bill sent successfully to {phone_no}")
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")

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
        tree = ttk.Treeview(frame, columns=("Slot", "Vehicle"), show="headings")
        tree.pack(side='left', fill='both', expand=True)

        # Set headings
        tree.heading("Slot", text="Slot")
        tree.heading("Vehicle", text="License Plate")

        # Dictionary to store level nodes
        level_nodes = {}

        # Insert level nodes into Treeview
        with open(self.parking_data1_file, 'r') as file:
            parked_vehicles = json.load(file)

            for level_data in parked_vehicles:
                level = f"Level {level_data['level']}"
                if level not in level_nodes:
                    # Add level as a parent node
                    level_node = tree.insert("", "end", values=(level, "-"))
                    level_nodes[level] = level_node

                # Populate the tree with parked vehicles
                for slot_data in level_data["slots"]:
                    slot = f"Slot {slot_data['slot']}"
                    vehicle_info = slot_data["vehicle"]
                    license_plate = vehicle_info["License Plate"] if vehicle_info else "-"
                    tree.insert(level_nodes[level], "end", values=(slot, license_plate))

        # Scrollbars for Treeview
        tree_scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree_scrollbar_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=tree_scrollbar_y.set)

        # tree_scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        # tree_scrollbar_x.pack(side="bottom", fill="x")
        # tree.configure(xscrollcommand=tree_scrollbar_x.set)

        # Close button
        close_button = ctk.CTkButton(self.vehicle_window, text="Close", command=self.close_vehicle_window)
        close_button.pack(pady=5)


    def close_vehicle_window(self):
        if self.vehicle_window is not None:
            self.vehicle_window.destroy()
            self.vehicle_window = None


    def search_vehicle(self):
        license_plate = self.search_vehicle_entry.get().strip()

        # Load parked vehicles from parking_data.json
        with open(self.data_file, 'r') as file:
            parked_vehicles = json.load(file)
            for vehicle in parked_vehicles:
                if vehicle["License Plate"] == license_plate:
                    vehicle_info = (
                        f"License Plate: {vehicle['License Plate']}\n"
                        f"Mobile Number: {vehicle['Mobile Number']}\n"
                        f"Vehicle Type: {vehicle['Vehicle Type']}\n"
                        f"Level: {vehicle['Level']}\n"
                        f"Slot: {vehicle['Slot']}\n"
                        f"Entry Date: {vehicle['Entry Date']}\n"
                        f"Entry Time: {vehicle['Entry Time']}"
                    )
                    messagebox.showinfo("Vehicle Found", vehicle_info)
                    return

        messagebox.showerror("Error", "Vehicle not found!")

    def check_parked_vehicles(self):
        current_time = datetime.now()
        notification_threshold = 6  # hours
        for index, vehicle_info in enumerate(self.parking_slots):
            if vehicle_info is not None:
                entry_time = datetime.strptime(vehicle_info["Entry Time"], "%H:%M:%S")
                entry_date = datetime.strptime(vehicle_info["Entry Date"], "%d-%m-%Y")
                duration = (current_time - entry_datetime).total_seconds() / 3600  # Convert seconds to hours        
                if duration > notification_threshold:
                    self.report_to_police(vehicle_info, index)
                    print(f"Vehicle {vehicle_info['License Plate']} standing at {vehicle_info['Level']} - Slot {index + 1} has been parked for over {notification_threshold} hours. Reported to police.")

    def report_to_police(self, vehicle_info, index):
        slot_index = f"Slot {index + 1}"
        entry_time = datetime.strptime(vehicle_info["Entry Time"], "%H:%M:%S")
        entry_date = datetime.strptime(vehicle_info["Entry Date"], "%d-%m-%Y")
        entry_datetime = datetime.combine(entry_date, entry_time.time())

        report_message = (
            f"Attention: Vehicle with License Plate {vehicle_info['License Plate']} has been parked for an extended period "
            f"exceeding the allowed 6 hours limit. \n"
            f"Details:\n"
            f"License Plate: {vehicle_info['License Plate']}\n"
            f"Vehicle Type: {vehicle_info['Vehicle Type']}\n"
            f"Mobile Number: {vehicle_info['Mobile Number']}\n"
            f"Entry Time: {entry_datetime.strftime("%H:%M:%S")}\n"
            f"Entry Date: {entry_datetime.strftime("%d-%m-%Y")}\n"
            f"Location: {vehicle_info['Level']} - {slot_index}\n"
            f"Please report the vehicle to police."
        )
        messagebox.showinfo("Vehicle Alert", report_message)

    def schedule_vehicle_checks(self):
        self.check_parked_vehicles()  # Perform an immediate check
        # Schedule the next check for 1 hour later
        self.after(3600000, self.schedule_vehicle_checks)


    def generate_parking_receipt_2(self, vehicle_info):
        global output_filename
        def format_mobile_number(mobile_number):
            if len(mobile_number) == 10:
                return f"{mobile_number[:2]}XXXXXX{mobile_number[-2:]}"
            return mobile_number  
        
        def format_duration(duration):
            months, days, hours, minutes, seconds = duration            
            total_days = months * 30 + days
            total_hours = total_days * 24 + hours
            return f"{total_hours} hours, {minutes} minutes, and {seconds} seconds"

        template_path = os.path.expanduser("F:/ParkingManagement/requirements/Blank_Receipt_watermark.pdf") 
        receipts_dir = os.path.expanduser("F:/ParkingManagement/receipts")
        os.makedirs(receipts_dir, exist_ok=True)
        output_filename = os.path.join(receipts_dir,f"Parking_Receipt_{vehicle_info['License Plate']}_{datetime.now().strftime('%H-%M-%S_%d-%m-%Y')}.pdf")
        
        billing_info_title = "Billing Information"
        c.setFont("Helvetica-Bold", 10)
        billing_info_y = parking_info_y - 55
        c.drawString(15, billing_info_y, billing_info_title)
        c.setFont("Helvetica", 8)
        c.drawString(15, billing_info_y - details_row_spacing, duration_text)
        cost_text = f"Subtotal: Rs. {vehicle_info['Cost']:.2f}"
        c.drawString(15, billing_info_y - details_row_spacing * 2, cost_text)
        cgst_text = f"CGST @ 9%: Rs. {vehicle_info['CGST']:.2f}"
        c.drawString(15, billing_info_y - details_row_spacing * 3, cgst_text)
        sgst_text = f"SGST @ 9%: Rs. {vehicle_info['SGST']:.2f}"
        c.drawString(15, billing_info_y - details_row_spacing * 3, sgst_text)
        total_text = f"Grand Total: Rs. {vehicle_info['Total Cost']:.2f}"
        c.drawString(15, billing_info_y - details_row_spacing * 4, total_text)
        employee_id_text = f"Employee ID: {self.current_user_instance.get_user().get('employee_id')}"
        c.drawString(15, billing_info_y - details_row_spacing * 5, employee_id_text)
        
        # Add a thank you message
        thank_you_text = "Thank you for parking with V-Park Parkings!"
        c.setFont("Helvetica", 8)
        thank_you_y = 30  # Adjust position as needed
        c.drawCentredString(page_width / 2, thank_you_y, thank_you_text)
        visit_again_text = "Visit Again!"
        c.setFont("Helvetica", 8)
        visit_again_y = 20  # Adjust position as needed
        c.drawCentredString(page_width / 2, visit_again_y, visit_again_text)

        receipt_gen_msg = f"This receipt was generated by {self.current_user_instance.get_user().get('employee_id')} on {datetime.now().strftime('%H:%M:%S %d-%m-%Y')}"
        c.setFont("Helvetica", 5)
        c.drawCentredString(page_width - 75, 3.25, receipt_gen_msg)

        # Save the PDF
        c.save()
        packet.seek(0)
        new_pdf = PdfReader(packet)
        page.merge_page(new_pdf.pages[0])

        # Write the modified content to a new file
        writer = PdfWriter()
        writer.add_page(page)
        with open(output_filename, 'wb') as f:
            writer.write(f)

        print("Parking receipt generated:", output_filename)
        return output_filename



    def generate_parking_receipt(self, vehicle_info):
        env_file = os.path.expanduser("F:/ParkingManagement/.data/.env")
        def initialize_serial_number():
            if 'VEHICLE_SERIAL_NUMBER' not in os.environ:
                set_key(env_file, 'VEHICLE_SERIAL_NUMBER', '10001')

        # Function to read the current serial number
        def read_serial_number():
            return int(os.getenv('VEHICLE_SERIAL_NUMBER', '10001'))

        # Function to increment and save the serial number
        def increment_serial_number():
            serial_number = read_serial_number()
            serial_number += 1
            set_key(env_file, 'VEHICLE_SERIAL_NUMBER', str(serial_number))
            return serial_number





if __name__ == "__main__":
    employee_file_path = os.path.expanduser("F:/ParkingManagement/.data/employee_data.json")
