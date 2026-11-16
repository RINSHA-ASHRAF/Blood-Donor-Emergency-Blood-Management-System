
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from main import Donor, load_donors, save_donors, BloodStock


# =========================================================
# DATA
# =========================================================

donors = load_donors()

blood_stock = BloodStock()
blood_stock.load_stock()


# =========================================================
# COLORS
# =========================================================

BG = "#F4F6FA"
WHITE = "#FFFFFF"
RED = "#C6284D"
DARK_RED = "#8E1538"
DARK = "#252A34"
TEXT = "#303642"
MUTED = "#7B8493"
GREEN = "#00897B"
BLUE = "#4054B2"
BORDER = "#E4E7EE"


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title("LifeLine | Blood Management System")
root.geometry("1100x700")
root.minsize(950, 600)
root.configure(bg=BG)


# =========================================================
# GENERAL FUNCTIONS
# =========================================================

def save_donor_data():
    save_donors(donors)


def save_blood_stock():
    blood_stock.save_stock()


def valid_blood_group(group):
    return group.strip().upper() in blood_stock.stock


def create_entry(parent, label_text, default_value=""):

    field_frame = tk.Frame(parent, bg=WHITE)
    field_frame.pack(fill="x", padx=20, pady=7)

    tk.Label(
        field_frame,
        text=label_text,
        font=("Arial", 10, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(anchor="w", pady=(0, 5))

    entry = tk.Entry(
        field_frame,
        font=("Arial", 11),
        relief="solid",
        bd=1
    )

    entry.pack(fill="x", ipady=6)

    if default_value != "":
        entry.insert(0, str(default_value))

    return entry


def create_form_window(title, height=520):

    window = tk.Toplevel(root)
    window.title(title)
    window.geometry(f"430x{height}")
    window.configure(bg=WHITE)
    window.resizable(False, False)

    tk.Label(
        window,
        text=title,
        font=("Arial", 18, "bold"),
        fg=DARK_RED,
        bg=WHITE
    ).pack(pady=18)

    return window


def show_message(title, message):

    messagebox.showinfo(
        title,
        message,
        parent=root
    )


# =========================================================
# REGISTER DONOR
# =========================================================

def open_register_form():

    window = create_form_window("Register New Donor", 600)

    donor_id_entry = create_entry(window, "Donor ID")
    name_entry = create_entry(window, "Full Name")
    age_entry = create_entry(window, "Age")
    blood_group_entry = create_entry(window, "Blood Group")
    phone_entry = create_entry(window, "Phone Number")
    location_entry = create_entry(window, "Location")

    def save_donor():

        try:
            donor_id = int(donor_id_entry.get())
            age = int(age_entry.get())

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Donor ID and age must be numbers.",
                parent=window
            )
            return

        name = name_entry.get().strip()
        blood_group = blood_group_entry.get().strip().upper()
        phone = phone_entry.get().strip()
        location = location_entry.get().strip()

        if not all([
            name,
            blood_group,
            phone,
            location
        ]):
            messagebox.showerror(
                "Missing Details",
                "Please fill all fields.",
                parent=window
            )
            return

        if age <= 0:
            messagebox.showerror(
                "Invalid Age",
                "Age must be greater than zero.",
                parent=window
            )
            return

        if not valid_blood_group(blood_group):
            messagebox.showerror(
                "Invalid Blood Group",
                "Enter a valid blood group such as A+, O-, or AB+.",
                parent=window
            )
            return

        for donor in donors:
            if donor.donor_id == donor_id:
                messagebox.showerror(
                    "Duplicate ID",
                    "This donor ID already exists.",
                    parent=window
                )
                return

        donor = Donor(
            donor_id,
            name,
            age,
            blood_group,
            phone,
            location
        )

        donors.append(donor)
        save_donor_data()

        refresh_dashboard()

        messagebox.showinfo(
            "Success",
            "Donor registered successfully!",
            parent=window
        )

        window.destroy()

    tk.Button(
        window,
        text="Save Donor",
        command=save_donor,
        font=("Arial", 11, "bold"),
        bg=RED,
        fg=WHITE,
        activebackground=DARK_RED,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        pady=9
    ).pack(fill="x", padx=20, pady=20)


# =========================================================
# VIEW DONORS
# =========================================================

def view_donors():

    # ---------------- VIEW DONORS WINDOW ----------------

    view_window = tk.Toplevel(root)

    view_window.title("View All Donors")
    view_window.geometry("1000x550")
    view_window.configure(bg="#F2F5FA")

    # ---------------- HEADER ----------------

    header = tk.Frame(
        view_window,
        bg="#8E1538",
        height=90
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Registered Donors",
        font=("Arial", 22, "bold"),
        fg="white",
        bg="#8E1538"
    ).pack(
        anchor="w",
        padx=25,
        pady=(15, 5)
    )

    tk.Label(
        header,
        text="Donor records arranged by Donor ID",
        font=("Arial", 11),
        fg="#F8DDE5",
        bg="#8E1538"
    ).pack(
        anchor="w",
        padx=27
    )

    # ---------------- TABLE FRAME ----------------

    table_frame = tk.Frame(
        view_window,
        bg="#F2F5FA"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    columns = (
        "ID",
        "Name",
        "Age",
        "Blood Group",
        "Phone",
        "Location"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    # ---------------- TABLE HEADINGS ----------------

    for column in columns:

        table.heading(
            column,
            text=column
        )

    table.column("ID", width=70, anchor="center")
    table.column("Name", width=180, anchor="center")
    table.column("Age", width=70, anchor="center")
    table.column("Blood Group", width=120, anchor="center")
    table.column("Phone", width=180, anchor="center")
    table.column("Location", width=250, anchor="center")

    # ---------------- TABLE SCROLLBAR ----------------

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=table.yview
    )

    table.configure(
        yscrollcommand=scrollbar.set
    )

    table.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # ---------------- DISPLAY DONORS ----------------

    if not donors:

        tk.Label(
            table_frame,
            text="No donors registered yet.",
            font=("Arial", 12),
            fg="#7B8493",
            bg="#F2F5FA"
        ).pack(pady=20)

    else:

        # Sort donors by numerical Donor ID
        sorted_donors = sorted(
            donors,
            key=lambda donor: int(donor.donor_id)
        )

        for donor in sorted_donors:

            table.insert(
                "",
                "end",
                values=(
                    donor.donor_id,
                    donor.name,
                    donor.age,
                    donor.blood_group,
                    donor.phone,
                    donor.location
                )
            )

    # ---------------- CLOSE BUTTON ----------------

    tk.Button(
        view_window,
        text="Close",
        command=view_window.destroy,
        bg="#8E1538",
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        padx=30,
        pady=8
    ).pack(pady=(0, 15))



# =========================================================
# SEARCH DONOR
# =========================================================

def search_donor():

    # ---------------- SEARCH DONOR WINDOW ----------------

    search_window = tk.Toplevel(root)

    search_window.title("Search Donor | LifeLine")
    search_window.geometry("1000x650")
    search_window.configure(bg="#F2F5FA")

    # ---------------- HEADER ----------------

    header = tk.Frame(
        search_window,
        bg="#8E1538",
        height=110
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Search Blood Donors",
        font=("Arial", 22, "bold"),
        fg="white",
        bg="#8E1538"
    ).pack(
        anchor="w",
        padx=30,
        pady=(20, 5)
    )

    tk.Label(
        header,
        text="Find donors by their blood group",
        font=("Arial", 11),
        fg="#F8DDE5",
        bg="#8E1538"
    ).pack(
        anchor="w",
        padx=32
    )

    # ---------------- SEARCH INPUT ----------------

    search_frame = tk.Frame(
        search_window,
        bg="white",
        highlightbackground="#E0E4EA",
        highlightthickness=1
    )

    search_frame.pack(
        fill="x",
        padx=25,
        pady=20
    )

    tk.Label(
        search_frame,
        text="Enter Blood Group",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#303642"
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )

    input_frame = tk.Frame(
        search_frame,
        bg="white"
    )

    input_frame.pack(
        fill="x",
        padx=15,
        pady=(0, 15)
    )

    blood_group_entry = tk.Entry(
        input_frame,
        font=("Arial", 13),
        relief="solid",
        bd=1
    )

    blood_group_entry.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=8
    )

    # ---------------- SEARCH RESULTS ----------------

    tk.Label(
        search_window,
        text="Search Results",
        font=("Arial", 17, "bold"),
        bg="#F2F5FA",
        fg="#303642"
    ).pack(
        anchor="w",
        padx=30,
        pady=(0, 10)
    )

    result_frame = tk.Frame(
        search_window,
        bg="#F2F5FA"
    )

    result_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 20)
    )

    columns = (
        "ID",
        "Name",
        "Age",
        "Blood Group",
        "Phone",
        "Location"
    )

    table = ttk.Treeview(
        result_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(
            column,
            text=column
        )

    table.column("ID", width=80, anchor="center")
    table.column("Name", width=180, anchor="center")
    table.column("Age", width=80, anchor="center")
    table.column("Blood Group", width=130, anchor="center")
    table.column("Phone", width=180, anchor="center")
    table.column("Location", width=250, anchor="center")

    scrollbar = ttk.Scrollbar(
        result_frame,
        orient="vertical",
        command=table.yview
    )

    table.configure(
        yscrollcommand=scrollbar.set
    )

    table.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # ---------------- NO DONORS MESSAGE ----------------

    no_donors_label = tk.Label(
        result_frame,
        text="",
        font=("Arial", 14, "bold"),
        fg="#8E1538",
        bg="#F2F5FA"
    )

    # ---------------- SEARCH FUNCTION ----------------

    def search_by_blood_group():

        group = blood_group_entry.get().strip().upper()

        if not group:

            messagebox.showwarning(
                "Missing Blood Group",
                "Please enter a blood group.",
                parent=search_window
            )

            return

        # Clear previous search results
        for item in table.get_children():
            table.delete(item)

        no_donors_label.config(text="")

        # Find matching donors
        matching_donors = [
            donor for donor in donors
            if donor.blood_group.strip().upper() == group
        ]

        if matching_donors:

            # Display donors in ascending Donor ID order
            matching_donors = sorted(
                matching_donors,
                key=lambda donor: int(donor.donor_id)
            )

            for donor in matching_donors:

                table.insert(
                    "",
                    "end",
                    values=(
                        donor.donor_id,
                        donor.name,
                        donor.age,
                        donor.blood_group,
                        donor.phone,
                        donor.location
                    )
                )

        else:

            no_donors_label.config(
                text=f"No donors available for blood group {group}."
            )

            no_donors_label.place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )

    # ---------------- SEARCH BUTTON ----------------

    tk.Button(
        input_frame,
        text="Search",
        command=search_by_blood_group,
        bg="#C7254E",
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        padx=30,
        pady=8
    ).pack(
        side="right",
        padx=(12, 0)
    )

    blood_group_entry.focus()

    search_window.grab_set()




# =========================================================
# UPDATE DONOR
# =========================================================


def update_donor():

    # ---------------- DONOR ID WINDOW ----------------

    id_window = tk.Toplevel(root)

    id_window.title("Update Donor")
    id_window.geometry("400x230")
    id_window.configure(bg="#F2F5FA")
    id_window.resizable(False, False)

    tk.Label(
        id_window,
        text="Update Donor",
        font=("Arial", 18, "bold"),
        fg="#8E1538",
        bg="#F2F5FA"
    ).pack(pady=(20, 10))

    tk.Label(
        id_window,
        text="Enter Donor ID:",
        font=("Arial", 11),
        bg="#F2F5FA"
    ).pack(pady=5)

    donor_id_entry = tk.Entry(
        id_window,
        font=("Arial", 12),
        width=25,
        relief="solid",
        bd=1
    )

    donor_id_entry.pack(pady=5)
    donor_id_entry.focus()

    # ---------------- CONTINUE BUTTON ----------------

    def submit_id():

        donor_id_text = donor_id_entry.get().strip()

        if not donor_id_text:
            messagebox.showerror(
                "Error",
                "Please enter a donor ID.",
                parent=id_window
            )
            return

        try:
            donor_id = int(donor_id_text)

        except ValueError:
            messagebox.showerror(
                "Invalid ID",
                "Donor ID must be a number.",
                parent=id_window
            )
            return

        # Find the donor
        donor = next(
            (d for d in donors if int(d.donor_id) == donor_id),
            None
        )

        if donor is None:
            messagebox.showerror(
                "Donor Not Found",
                "No donor found with this ID.",
                parent=id_window
            )
            return

        # Close the ID window
        id_window.destroy()

        # ---------------- UPDATE FORM ----------------

        update_window = tk.Toplevel(root)

        update_window.title("Edit Donor Details")
        update_window.geometry("450x600")
        update_window.configure(bg="#F2F5FA")
        update_window.resizable(False, False)

        tk.Label(
            update_window,
            text="Edit Donor Details",
            font=("Arial", 20, "bold"),
            fg="#8E1538",
            bg="#F2F5FA"
        ).pack(pady=20)

        entries = {}

        fields = [
            ("Name", donor.name),
            ("Age", donor.age),
            ("Blood Group", donor.blood_group),
            ("Phone", donor.phone),
            ("Location", donor.location)
        ]

        for field, value in fields:

            tk.Label(
                update_window,
                text=field,
                font=("Arial", 11, "bold"),
                bg="#F2F5FA"
            ).pack(pady=(8, 3))

            entry = tk.Entry(
                update_window,
                font=("Arial", 12),
                width=30,
                relief="solid",
                bd=1
            )

            entry.pack(ipady=5)

            entry.insert(0, str(value))

            entries[field] = entry

        # ---------------- SAVE CHANGES ----------------

        def save_changes():

            name = entries["Name"].get().strip()
            age_text = entries["Age"].get().strip()
            blood_group = entries["Blood Group"].get().strip().upper()
            phone = entries["Phone"].get().strip()
            location = entries["Location"].get().strip()

            if not all([
                name,
                age_text,
                blood_group,
                phone,
                location
            ]):
                messagebox.showerror(
                    "Missing Details",
                    "Please fill all fields.",
                    parent=update_window
                )
                return

            try:
                age = int(age_text)

            except ValueError:
                messagebox.showerror(
                    "Invalid Age",
                    "Age must be a number.",
                    parent=update_window
                )
                return

            if age <= 0:
                messagebox.showerror(
                    "Invalid Age",
                    "Age must be greater than zero.",
                    parent=update_window
                )
                return

            valid_groups = [
                "A+", "A-", "B+", "B-",
                "AB+", "AB-", "O+", "O-"
            ]

            if blood_group not in valid_groups:
                messagebox.showerror(
                    "Invalid Blood Group",
                    "Enter a valid blood group.",
                    parent=update_window
                )
                return

            # Update donor object
            donor.name = name
            donor.age = age
            donor.blood_group = blood_group
            donor.phone = phone
            donor.location = location

            # Save updated donor information
            save_donors(donors)

            messagebox.showinfo(
                "Success",
                "Donor details updated successfully!",
                parent=update_window
            )

            update_window.destroy()

        tk.Button(
            update_window,
            text="Save Changes",
            command=save_changes,
            bg="#8E1538",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            padx=25,
            pady=10
        ).pack(pady=25)

    # ---------------- BUTTON ----------------

    tk.Button(
        id_window,
        text="Continue",
        command=submit_id,
        bg="#8E1538",
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        padx=25,
        pady=8
    ).pack(pady=15)

    id_window.grab_set()

# =========================================================
# DELETE DONOR
# =========================================================

def delete_donor():

    # ---------------- DONOR ID WINDOW ----------------

    id_window = tk.Toplevel(root)

    id_window.title("Delete Donor")
    id_window.geometry("400x250")
    id_window.configure(bg="#F2F5FA")
    id_window.resizable(False, False)

    tk.Label(
        id_window,
        text="Delete Donor",
        font=("Arial", 18, "bold"),
        fg="#8E1538",
        bg="#F2F5FA"
    ).pack(pady=(20, 10))

    tk.Label(
        id_window,
        text="Enter Donor ID:",
        font=("Arial", 11),
        bg="#F2F5FA"
    ).pack(pady=5)

    donor_id_entry = tk.Entry(
        id_window,
        font=("Arial", 12),
        width=25,
        relief="solid",
        bd=1
    )

    donor_id_entry.pack(pady=5)
    donor_id_entry.focus()

    # ---------------- DELETE DONOR ----------------

    def submit_id():

        donor_id_text = donor_id_entry.get().strip()

        if not donor_id_text:
            messagebox.showerror(
                "Missing ID",
                "Please enter a donor ID.",
                parent=id_window
            )
            return

        try:
            donor_id = int(donor_id_text)

        except ValueError:
            messagebox.showerror(
                "Invalid ID",
                "Donor ID must be a number.",
                parent=id_window
            )
            return

        donor = next(
            (d for d in donors if int(d.donor_id) == donor_id),
            None
        )

        if donor is None:
            messagebox.showerror(
                "Donor Not Found",
                "No donor found with this ID.",
                parent=id_window
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Donor Name: {donor.name}\n"
            f"Blood Group: {donor.blood_group}\n\n"
            "Are you sure you want to delete this donor?",
            parent=id_window
        )

        if confirm:

            donors.remove(donor)

            save_donors(donors)

            messagebox.showinfo(
                "Success",
                "Donor deleted successfully!",
                parent=id_window
            )

            id_window.destroy()

    # ---------------- BUTTON ----------------

    tk.Button(
        id_window,
        text="Delete Donor",
        command=submit_id,
        bg="#8E1538",
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        padx=25,
        pady=8
    ).pack(pady=20)

    id_window.grab_set()



# =========================================================
# ADD BLOOD STOCK
# =========================================================


def add_blood_stock():

    # ---------------- BLOOD STOCK WINDOW ----------------

    stock_window = tk.Toplevel(root)

    stock_window.title("Add Blood Stock")
    stock_window.geometry("450x350")
    stock_window.configure(bg="#F2F5FA")
    stock_window.resizable(False, False)

    # ---------------- COMBOBOX STYLE ----------------

    style = ttk.Style()

    style.theme_use("clam")

    style.configure(
        "Blood.TCombobox",
        fieldbackground="white",
        background="#8E1538",
        foreground="#303642",
        arrowcolor="white"
    )

    style.map(
        "Blood.TCombobox",
        fieldbackground=[
            ("readonly", "white")
        ],
        foreground=[
            ("readonly", "#303642")
        ],
        selectbackground=[
            ("readonly", "#8E1538")
        ],
        selectforeground=[
            ("readonly", "white")
        ]
    )

    # ---------------- HEADING ----------------

    tk.Label(
        stock_window,
        text="Add Blood Stock",
        font=("Arial", 20, "bold"),
        fg="#8E1538",
        bg="#F2F5FA"
    ).pack(pady=(20, 15))

    # ---------------- BLOOD GROUP ----------------

    tk.Label(
        stock_window,
        text="Select Blood Group",
        font=("Arial", 11, "bold"),
        bg="#F2F5FA"
    ).pack(pady=5)

    blood_group_combo = ttk.Combobox(
        stock_window,
        values=list(blood_stock.stock.keys()),
        state="readonly",
        font=("Arial", 12),
        width=25,
        style="Blood.TCombobox"
    )

    blood_group_combo.pack(
        pady=5,
        ipady=5
    )

    # ---------------- UNITS ----------------

    tk.Label(
        stock_window,
        text="Number of Units",
        font=("Arial", 11, "bold"),
        bg="#F2F5FA"
    ).pack(pady=10)

    units_entry = tk.Entry(
        stock_window,
        font=("Arial", 12),
        width=28,
        relief="solid",
        bd=1
    )

    units_entry.pack(
        pady=5,
        ipady=5
    )

    # ---------------- ADD STOCK FUNCTION ----------------

    def save_stock():

        group = blood_group_combo.get().strip()
        units_text = units_entry.get().strip()

        if not group:

            messagebox.showerror(
                "Missing Blood Group",
                "Please select a blood group.",
                parent=stock_window
            )

            return

        try:
            units = int(units_text)

        except ValueError:

            messagebox.showerror(
                "Invalid Units",
                "Please enter a whole number.",
                parent=stock_window
            )

            return

        if units <= 0:

            messagebox.showerror(
                "Invalid Units",
                "Units must be greater than zero.",
                parent=stock_window
            )

            return

        # Add the units to the existing stock
        blood_stock.add_blood(group, units)

        # Save the updated stock to the file
        save_blood_stock()

        messagebox.showinfo(
            "Success",
            f"{units} units of {group} added successfully!",
            parent=stock_window
        )

        stock_window.destroy()

    # ---------------- ADD STOCK BUTTON ----------------

    tk.Button(
        stock_window,
        text="Add Stock",
        command=save_stock,
        bg="#008F83",
        fg="white",
        font=("Arial", 12, "bold"),
        relief="flat",
        padx=30,
        pady=10
    ).pack(pady=25)

    stock_window.grab_set()




# =========================================================
# VIEW BLOOD STOCK
# =========================================================

def view_blood_stock():

    window = tk.Toplevel(root)
    window.title("Blood Stock")
    window.geometry("450x500")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="Blood Stock Inventory",
        font=("Arial", 20, "bold"),
        fg=DARK_RED,
        bg=BG
    ).pack(pady=20)

    table = ttk.Treeview(
        window,
        columns=("Group", "Units"),
        show="headings",
        height=8
    )

    table.heading("Group", text="Blood Group")
    table.heading("Units", text="Available Units")

    table.column("Group", anchor="center", width=180)
    table.column("Units", anchor="center", width=180)

    table.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=15
    )

    for group, units in blood_stock.stock.items():
        table.insert(
            "",
            "end",
            values=(group, units)
        )


# =========================================================
# EMERGENCY BLOOD REQUEST
# =========================================================


def emergency_blood_request():

    # ---------------- EMERGENCY REQUEST WINDOW ----------------

    request_window = tk.Toplevel(root)

    request_window.title("Emergency Blood Request")
    request_window.geometry("450x380")
    request_window.configure(bg="#F2F5FA")
    request_window.resizable(False, False)

    tk.Label(
        request_window,
        text="Emergency Blood Request",
        font=("Arial", 19, "bold"),
        fg="#8E1538",
        bg="#F2F5FA"
    ).pack(pady=(20, 15))

    # ---------------- BLOOD GROUP ----------------

    tk.Label(
        request_window,
        text="Required Blood Group",
        font=("Arial", 11, "bold"),
        bg="#F2F5FA"
    ).pack(pady=5)

    blood_group_combo = ttk.Combobox(
        request_window,
        values=list(blood_stock.stock.keys()),
        state="readonly",
        font=("Arial", 12),
        width=25
    )

    blood_group_combo.pack(pady=5, ipady=5)

    # ---------------- REQUIRED UNITS ----------------

    tk.Label(
        request_window,
        text="Number of Units Required",
        font=("Arial", 11, "bold"),
        bg="#F2F5FA"
    ).pack(pady=10)

    units_entry = tk.Entry(
        request_window,
        font=("Arial", 12),
        width=28,
        relief="solid",
        bd=1
    )

    units_entry.pack(pady=5, ipady=5)

    # ---------------- LARGE INSUFFICIENT STOCK WINDOW ----------------

    def show_insufficient_stock(group, available, required):

        shortage = required - available

        stock_window = tk.Toplevel(request_window)

        stock_window.title("Insufficient Blood Stock")
        stock_window.geometry("450x350")
        stock_window.configure(bg="#F2F5FA")
        stock_window.resizable(False, False)

        tk.Label(
            stock_window,
            text="Insufficient Blood Stock",
            font=("Arial", 18, "bold"),
            fg="#C62828",
            bg="#F2F5FA"
        ).pack(pady=(25, 10))

        tk.Label(
            stock_window,
            text="The requested blood units are not available.",
            font=("Arial", 11),
            fg="#555555",
            bg="#F2F5FA"
        ).pack(pady=5)

        # Information card
        details_frame = tk.Frame(
            stock_window,
            bg="white",
            highlightbackground="#E0E4EA",
            highlightthickness=1
        )

        details_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        details = [
            ("Blood Group", group),
            ("Available Units", available),
            ("Required Units", required),
            ("Shortage", shortage)
        ]

        for label_text, value in details:

            row = tk.Frame(
                details_frame,
                bg="white"
            )

            row.pack(
                fill="x",
                padx=15,
                pady=8
            )

            tk.Label(
                row,
                text=label_text,
                font=("Arial", 11),
                bg="white",
                fg="#303642"
            ).pack(side="left")

            tk.Label(
                row,
                text=str(value),
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#C62828"
            ).pack(side="right")

        tk.Button(
            stock_window,
            text="OK",
            command=stock_window.destroy,
            bg="#8E1538",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=35,
            pady=8
        ).pack(pady=10)

        stock_window.transient(request_window)
        stock_window.grab_set()

    # ---------------- SUBMIT REQUEST ----------------

    def submit_request():

        group = blood_group_combo.get().strip()
        units_text = units_entry.get().strip()

        if not group:
            messagebox.showerror(
                "Missing Blood Group",
                "Please select a blood group.",
                parent=request_window
            )
            return

        try:
            units = int(units_text)

        except ValueError:
            messagebox.showerror(
                "Invalid Units",
                "Please enter a whole number.",
                parent=request_window
            )
            return

        if units <= 0:
            messagebox.showerror(
                "Invalid Units",
                "Units must be greater than zero.",
                parent=request_window
            )
            return

        available_units = blood_stock.stock[group]

        if available_units >= units:

            blood_stock.stock[group] -= units

            save_blood_stock()

            remaining_units = blood_stock.stock[group]

            messagebox.showinfo(
                "Request Successful",
                f"Blood Group: {group}\n"
                f"Requested Units: {units}\n"
                f"Remaining Units: {remaining_units}",
                parent=request_window
            )

            request_window.destroy()

        else:

            show_insufficient_stock(
                group,
                available_units,
                units
            )

    # ---------------- SUBMIT BUTTON ----------------

    tk.Button(
        request_window,
        text="Submit Request",
        command=submit_request,
        bg="#D63D43",
        fg="white",
        font=("Arial", 12, "bold"),
        relief="flat",
        padx=30,
        pady=10
    ).pack(pady=25)

    request_window.grab_set()




# =========================================================
# EXIT
# =========================================================

def exit_application():

    if messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    ):
        root.destroy()


# =========================================================
# STYLES
# =========================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=TEXT,
    rowheight=30,
    fieldbackground=WHITE,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background=DARK_RED,
    foreground=WHITE,
    font=("Arial", 10, "bold")
)

style.map(
    "Treeview",
    background=[("selected", RED)],
    foreground=[("selected", WHITE)]
)


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(
    root,
    bg=DARK_RED,
    height=100
)

header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="❤  LIFELINE",
    font=("Arial", 25, "bold"),
    fg=WHITE,
    bg=DARK_RED
).pack(
    anchor="w",
    padx=30,
    pady=(15, 0)
)

tk.Label(
    header,
    text="Blood Donor & Emergency Blood Management System",
    font=("Arial", 11),
    fg="#F8DDE5",
    bg=DARK_RED
).pack(
    anchor="w",
    padx=33
)


# =========================================================
# MAIN LAYOUT
# =========================================================

body = tk.Frame(
    root,
    bg=BG
)

body.pack(fill="both", expand=True)


# =========================================================
# SIDEBAR
# =========================================================

sidebar = tk.Frame(
    body,
    bg=DARK,
    width=230
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="MAIN MENU",
    font=("Arial", 10, "bold"),
    fg="#AEB4C0",
    bg=DARK
).pack(
    anchor="w",
    padx=25,
    pady=(30, 15)
)


def sidebar_button(label, command):

    button = tk.Button(
        sidebar,
        text=label,
        command=command,
        font=("Arial", 11),
        bg=DARK,
        fg=WHITE,
        activebackground=RED,
        activeforeground=WHITE,
        relief="flat",
        anchor="w",
        padx=22,
        pady=12,
        cursor="hand2",
        bd=0
    )

    button.pack(fill="x", padx=8, pady=2)


sidebar_button("  Register Donor", open_register_form)
sidebar_button("  View Donors", view_donors)
sidebar_button("  Search Donor", search_donor)
sidebar_button("  Update Donor", update_donor)
sidebar_button("  Delete Donor", delete_donor)
sidebar_button("  Add Blood Stock", add_blood_stock)
sidebar_button("  View Blood Stock", view_blood_stock)
sidebar_button("  Emergency Request", emergency_blood_request)

tk.Button(
    sidebar,
    text="  Exit Application",
    command=exit_application,
    font=("Arial", 11),
    bg="#424854",
    fg=WHITE,
    activebackground=RED,
    activeforeground=WHITE,
    relief="flat",
    anchor="w",
    padx=22,
    pady=12,
    cursor="hand2",
    bd=0
).pack(
    side="bottom",
    fill="x",
    padx=8,
    pady=15
)


# =========================================================
# DASHBOARD
# =========================================================

content = tk.Frame(
    body,
    bg=BG
)

content.pack(
    side="left",
    fill="both",
    expand=True,
    padx=30,
    pady=25
)

tk.Label(
    content,
    text="Dashboard",
    font=("Arial", 24, "bold"),
    fg=TEXT,
    bg=BG
).pack(anchor="w")

tk.Label(
    content,
    text="Manage donors, blood inventory, and emergency requests.",
    font=("Arial", 11),
    fg=MUTED,
    bg=BG
).pack(
    anchor="w",
    pady=(5, 20)
)


# =========================================================
# DASHBOARD CARDS
# =========================================================

cards_frame = tk.Frame(
    content,
    bg=BG
)

cards_frame.pack(fill="x", pady=10)


def create_card(parent, title, value, color):

    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=7
    )

    tk.Label(
        card,
        text=title,
        font=("Arial", 10, "bold"),
        fg=MUTED,
        bg=WHITE
    ).pack(
        anchor="w",
        padx=15,
        pady=(15, 5)
    )

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 25, "bold"),
        fg=color,
        bg=WHITE
    )

    value_label.pack(
        anchor="w",
        padx=15,
        pady=(0, 15)
    )

    return value_label


donor_count_label = create_card(
    cards_frame,
    "REGISTERED DONORS",
    str(len(donors)),
    RED
)

blood_group_count_label = create_card(
    cards_frame,
    "BLOOD GROUPS",
    str(len(blood_stock.stock)),
    BLUE
)

stock_count_label = create_card(
    cards_frame,
    "AVAILABLE UNITS",
    str(sum(blood_stock.stock.values())),
    GREEN
)


def refresh_dashboard():

    donor_count_label.config(
        text=str(len(donors))
    )

    blood_group_count_label.config(
        text=str(len(blood_stock.stock))
    )

    stock_count_label.config(
        text=str(sum(blood_stock.stock.values()))
    )


# =========================================================
# QUICK ACTIONS
# =========================================================

tk.Label(
    content,
    text="Quick Actions",
    font=("Arial", 17, "bold"),
    fg=TEXT,
    bg=BG
).pack(
    anchor="w",
    pady=(25, 12)
)

actions_frame = tk.Frame(
    content,
    bg=BG
)

actions_frame.pack(fill="x")


def action_button(parent, text, command, color):

    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 11, "bold"),
        bg=color,
        fg=WHITE,
        activebackground=DARK_RED,
        activeforeground=WHITE,
        relief="flat",
        height=2,
        cursor="hand2",
        bd=0
    )


action_button(
    actions_frame,
    "＋  Register New Donor",
    open_register_form,
    RED
).grid(
    row=0,
    column=0,
    sticky="ew",
    padx=7,
    pady=7
)

action_button(
    actions_frame,
    "▣  View All Donors",
    view_donors,
    BLUE
).grid(
    row=0,
    column=1,
    sticky="ew",
    padx=7,
    pady=7
)

action_button(
    actions_frame,
    "＋  Add Blood Stock",
    add_blood_stock,
    GREEN
).grid(
    row=1,
    column=0,
    sticky="ew",
    padx=7,
    pady=7
)

action_button(
    actions_frame,
    "♥  Emergency Request",
    emergency_blood_request,
    "#D84343"
).grid(
    row=1,
    column=1,
    sticky="ew",
    padx=7,
    pady=7
)

actions_frame.columnconfigure(0, weight=1)
actions_frame.columnconfigure(1, weight=1)


# =========================================================
# FOOTER
# =========================================================

tk.Label(
    content,
    text="LifeLine  |  Every Drop Counts",
    font=("Arial", 10, "italic"),
    fg=MUTED,
    bg=BG
).pack(
    side="bottom",
    anchor="w",
    pady=10
)


# =========================================================
# RUN APPLICATION
# =========================================================

root.mainloop()
