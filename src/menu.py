class Menu:
    def __init__(self, db_operations):
        self.db_operations = db_operations

    def display_menu(self):
        print("\nMenu:")
        print("**********")
        print(" 1. Create table FlightInfo")
        print(" 2. Insert data into FlightInfo")
        print(" 3. Select all data from FlightInfo")
        print(" 4. Search a flight")
        print(" 5. Update data some records")
        print(" 6. Delete data some records")
        print(" 7. Exit\n")

    def run(self):
        while True:
            self.display_menu()
            choice = int(input("Enter your choice: "))
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
                exit(0)
            else:
                print("Invalid Choice")