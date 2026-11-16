class Donor:

    def __init__(self, donor_id, name, age, blood_group, phone, location):
        self.donor_id = donor_id
        self.name = name
        self.age = age
        self.blood_group = blood_group
        self.phone = phone
        self.location = location

    def display_details(self):
        print("\n----- DONOR DETAILS -----")
        print("Donor ID    :", self.donor_id)
        print("Name        :", self.name)
        print("Age         :", self.age)
        print("Blood Group :", self.blood_group)
        print("Phone       :", self.phone)
        print("Location    :", self.location)

class BloodStock:

    def __init__(self):
        self.stock = {
            "A+": 0,
            "A-": 0,
            "B+": 0,
            "B-": 0,
            "AB+": 0,
            "AB-": 0,
            "O+": 0,
            "O-": 0
        }

    def add_blood(self, blood_group, units):

        if blood_group in self.stock:

            self.stock[blood_group] += units
            self.save_stock()

            print("\nBlood stock updated successfully!")

        else:

            print("\nInvalid blood group.")

    def display_stock(self):

        print("\n========== BLOOD STOCK ==========")

        for blood_group, units in self.stock.items():

            print(blood_group, ":", units, "units")

    def save_stock(self):

        with open("blood_stock.txt", "w") as file:

            for blood_group, units in self.stock.items():
                file.write(f"{blood_group},{units}\n")

        print("Blood stock saved successfully!")

    def load_stock(self):

        try:
            with open("blood_stock.txt", "r") as file:

                for line in file:
                    data = line.strip().split(",")

                    blood_group = data[0]
                    units = int(data[1])

                    if blood_group in self.stock:
                        self.stock[blood_group] = units

        except FileNotFoundError:
            print("Blood stock file not found. Starting with zero stock.")

def register_donor(donors):

    print("\n----- REGISTER DONOR -----")

    donor_id = int(input("Enter Donor ID: "))
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    blood_group = input("Enter Blood Group: ")
    phone = input("Enter Phone Number: ")
    location = input("Enter Location: ")

    donor = Donor(
        donor_id,
        name,
        age,
        blood_group,
        phone,
        location
    )

    donors.append(donor)
    save_donors(donors)

    print("\nDonor registered successfully!")

def view_donors(donors):

    if len(donors) == 0:
        print("\nNo donors registered yet.")
        return

    print("\n========== ALL DONORS ==========")

    for donor in donors:
        donor.display_details()


def search_donor(donors):

    blood_group = input("Enter required blood group: ")

    found = False

    for donor in donors:

        if donor.blood_group.upper() == blood_group.upper():
            donor.display_details()
            found = True

    if found == False:
        print("\nNo donor found for this blood group.")

def update_donor(donors):

    donor_id = int(input("\nEnter Donor ID to update: "))

    found = False

    for donor in donors:

        if donor.donor_id == donor_id:

            print("\nDonor found!")
            donor.display_details()

            print("\nEnter new details")

            donor.name = input("Enter Name: ")
            donor.age = int(input("Enter Age: "))
            donor.blood_group = input("Enter Blood Group: ")
            donor.phone = input("Enter Phone Number: ")
            donor.location = input("Enter Location: ")

            print("\nDonor details updated successfully!")

            found = True
            break

    if found == False:
        print("\nDonor ID not found.")

def delete_donor(donors):

    donor_id = int(input("\nEnter Donor ID to delete: "))

    for donor in donors:

        if donor.donor_id == donor_id:

            print("\nDonor found!")
            donor.display_details()

            confirmation = input(
                "\nAre you sure you want to delete this donor? (yes/no): "
            )

            if confirmation.lower() == "yes":

                donors.remove(donor)

                print("\nDonor deleted successfully!")

            else:

                print("\nDeletion cancelled.")

            return

    print("\nDonor ID not found.")

def add_blood_stock(blood_stock):

    print("\n----- ADD BLOOD STOCK -----")

    blood_group = input("Enter Blood Group: ").upper()

    units = int(input("Enter Number of Units: "))

    blood_stock.add_blood(blood_group, units)


def emergency_blood_request(blood_stock):

    blood_group = input("Enter required blood group: ").upper()

    try:
        units = int(input("Enter number of units required: "))

        if units <= 0:
            print("Units must be greater than zero.")
            return

        if blood_group not in blood_stock.stock:
            print("Invalid blood group.")
            return

        available_units = blood_stock.stock[blood_group]

        if available_units >= units:

            print("\nSufficient blood stock is available!")
            print("Blood Group:", blood_group)
            print("Available Units:", available_units)
            print("Required Units:", units)
            blood_stock.stock[blood_group] -= units
            blood_stock.save_stock()
            

        else:
            print("\nInsufficient blood stock!")
            print("Blood Group:", blood_group)
            print("Available Units:", available_units)
            print("Required Units:", units)
            print("Shortage:", units - available_units, "units")

    except ValueError:
        print("Please enter a valid number of units.")



def save_donors(donors):

    with open("donors.txt", "w") as file:

        for donor in donors:
            file.write(
                f"{donor.donor_id},{donor.name},{donor.age},"
                f"{donor.blood_group},{donor.phone},{donor.location}\n"
            )

    print("Donor details saved successfully!")




def load_donors():

    donors = []

    try:
        with open("donors.txt", "r") as file:

            for line in file:

                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                data = line.split(",")

                # Skip invalid records
                if len(data) != 6:
                    continue

                donor = Donor(
                    int(data[0]),
                    data[1],
                    int(data[2]),
                    data[3],
                    data[4],
                    data[5]
                )

                donors.append(donor)

    except FileNotFoundError:
        # If the file does not exist, start with an empty list
        pass

    return donors



def main():


    donors = load_donors()
    blood_stock = BloodStock()
    blood_stock.load_stock()

    while True:

        print("\n========================================")
        print("     BLOOD DONOR MANAGEMENT SYSTEM")
        print("========================================")
        print("1. Register Donor")
        print("2. View All Donors")
        print("3. Search Donor")
        print("4. Update Donor")
        print("5. Delete Donor")
        print("6. Add Blood Stock")
        print("7. View Blood Stock")
        print("8. Emergency Blood Request")
        print("9. Exit")
        print("========================================")

        choice = input("Enter your choice: ")

        
        if choice == "1":

            register_donor(donors)

        
        elif choice == "2":

            view_donors(donors)

        
        elif choice == "3":

            search_donor(donors)

        elif choice == "4":

            update_donor(donors)

        elif choice == "5":
        
             delete_donor(donors)
        elif choice == "6":

            add_blood_stock(blood_stock)

        elif choice == "7":
            blood_stock.display_stock()

        elif choice == "8":
            emergency_blood_request(blood_stock)

        elif choice == "9":

            print("\nThank you for using the system!")
            break


if __name__ == "__main__":
    main()
