from flight_info import FlightInfo
from db_operations import DBOperations

class Menu:
    def __init__(self, db_filename):
        self.db_operations = DBOperations(db_filename)
        self.db_operations.connect()
        self.flight_info = FlightInfo(db_filename)

        self.main_menu_items = [
            {"option": 1, "description": "Manage Flights", "function": self.handle_flights_menu},
            {"option": 2, "description": "Manage Pilots", "function": self.handle_pilots_menu},
            {"option": 3, "description": "Manage Schedules", "function": self.handle_schedules_menu},
            {"option": 7, "description": "Exit", "function": self.exit_program},
        ]

        self.flights_menu_items = [
            {"option": 1, "description": "Create Flights Table", "function": self.create_flights_table},
            {"option": 3, "description": "View Flights by Criteria", "function": self.view_flights_by_criteria},
            {"option": 8, "description": "Back to Main Menu", "function": self.display_menu},
        ]

    def getInput(self, prompt):
        while True:
            try:
                value = input(prompt)
                if not value.strip():
                    raise ValueError("Input cannot be empty")
                return value
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    def display_menu(self, menu_items):
        print("\nMenu:")
        print("**********")
        for item in menu_items:
            print(f" {item['option']}. {item['description']}")
        print("\n")

    def run(self):
        while True:
            self.display_menu(self.main_menu_items)
            choice = int(input("Enter your choice: "))
            for item in self.main_menu_items:
                if item["option"] == choice:
                    item["function"]()
                    break
            else:
                print("Invalid choice. Please try again.")

    def handle_flights_menu(self):
        while True:
            self.display_menu(self.flights_menu_items)
            choice = int(input("Enter your choice for Flights Menu: "))
            for item in self.flights_menu_items:
                if item["option"] == choice:
                    item["function"]()
                    break
            else:
                print("Invalid choice. Please try again.")

    def create_flights_table(self):
        print("Creating Flights Table...")

    def view_flights_by_criteria(self):
        self.flight_info.view_flights_by_criteria()

    def handle_pilots_menu(self):
        print("Handling Pilots Menu...")

    def handle_schedules_menu(self):
        print("Handling Schedules Menu...")

    def exit_program(self):
        print("Exiting program...")
        self.db_operations.close()
        exit()