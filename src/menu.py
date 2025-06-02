class Menu:
    def __init__(self, db_operations):
        self.db_operations = db_operations

    def display_main_menu(self):
        print("\nMain Menu:")
        print("**********")
        print(" 1. Manage Flights")
        print(" 2. Insert data into FlightInfo")
        print(" 3. Select all data from FlightInfo")
        print(" 4. Search a flight")
        print(" 5. Update data some records")
        print(" 6. Delete data some records")
        print(" 7. Exit\n")

    def display_flights_menu(self):
        print("\nFlights Menu:")
        print("**********")
        print(" 1. Create table Flights")
        print(" 2. Insert data into Flights")
        print(" 3. Select all data from Flights")
        print(" 4. Search a flight")
        print(" 5. Update data some records")
        print(" 6. Delete data some records")
        print (" 7. Print all flights")
        print(" 8. Back to Main Menu\n")

    def handle_flights_menu(self):
        while True:
            self.display_flights_menu()
            try:
                choice = int(input("Enter your choice for Flights Menu: "))
                self.db_operations.connect() 
                if choice == 1:
                    self.db_operations.create_table()
                elif choice == 2:
                    self.db_operations.insert_data()
                elif choice == 3:
                    self.db_operations.select_all()
                elif choice == 4:
                    self.db_operations.search_data()
                elif choice == 5:
                    self.db_operations.update_data()
                elif choice == 6:
                    self.db_operations.delete_data()
                elif choice == 7:
                    self.db_operations.print_all('flights')
                elif choice == 8:
                    break  # Return to the main menu
                else:
                    print("Invalid Choice")
            finally:
                self.db_operations.close()
    def run(self):
        while True:
            self.display_main_menu()
            choice = int(input("Enter your choice: "))
            if choice == 1:
                self.handle_flights_menu()  # Navigate to the Flights submenu
            elif choice == 2:
                self.db_operations.insert_data()
            elif choice == 3:
                self.db_operations.select_all()
            elif choice == 4:
                self.db_operations.search_data()
            elif choice == 5:
                self.db_operations.update_data()
            elif choice == 6:
                self.db_operations.delete_data()
            elif choice == 7:
                exit(0)
            else:
                print("Invalid Choice")