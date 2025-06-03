from flight_info import FlightInfo
from pilots import Pilots
from db_operations import DBOperations

class Menu:
    def __init__(self, db_filename):
        self.db_operations = DBOperations(db_filename)
        self.db_operations.connect()
        self.flight_info = FlightInfo(db_filename)
        self.pilots = Pilots(db_filename)

        self.main_menu_items = [
            {"option": 1, "description": "Manage Flights", "function": self.handle_flights_menu},
            {"option": 2, "description": "Manage Pilots", "function": self.handle_pilots_menu},
            {"option": 3, "description": "Manage Schedules", "function": self.handle_schedules_menu},
            {"option": 7, "description": "Exit", "function": self.exit_program},
        ]

        self.flights_menu_items = [
            {"option": 1, "description": "Create Flights Table", "function": self.create_flights_table},
            {"option": 2, "description": "Add a new flight", "function": self.create_flight},
            {"option": 3, "description": "View Flights by Criteria", "function": self.view_flights_by_criteria},
            {"option": 4, "description": "Updte Flight Information", "function": self.update_flight_information},
            {"option": 8, "description": "Back to Main Menu", "function": self.go_back_to_main_menu},
        ]

        self.pilots_menu_items = [
            {"option": 1, "description": "View Pilots", "function": self.view_pilots},
            {"option": 2, "description": "Add Pilot", "function": self.add_pilot},
            {"option": 3, "description": "Update Pilot Information", "function": self.update_pilot_information},
            {"option": 4, "description": "Delete Pilot", "function": self.delete_pilot},
            {"option": 5, "description": "Assign Pilot to flight", "function": self.assign_pilot_to_flight},
            {"option": 7, "description": "Remove Pilot from flight", "function": self.remove_pilot_from_flight},
            {"option": 8, "description": "Display Pilot Schedule", "function": self.get_pilot_schedule},
            {"option": 9, "description": "Back to Main Menu", "function": self.go_back_to_main_menu},
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

    def handle_main_menu(self):
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
        
    def create_flight(self):
        self.flight_info.create_flight()
    
    def update_flight_information(self):
        self.flight_info.update_flight_information()

    def handle_pilots_menu(self):
        while True:
            self.display_menu(self.pilots_menu_items)
            choice = int(input("Enter your choice for Pilots Menu: "))
            for item in self.pilots_menu_items:
                if item["option"] == choice:
                    item["function"]()
                    break
            else:
                print("Invalid choice. Please try again.")
                
    def handle_schedules_menu(self):
        print("Handling Schedules Menu...")

    def view_pilots(self):
        self.pilots.view_pilot()
    
    def add_pilot(self):
        print("Adding Pilot...")
    
    def update_pilot_information(self):
        print("Updating Pilot Information...")
    
    def delete_pilot(self):
        print("Deleting Pilot...")

    def assign_pilot_to_flight(self):
        print("Assigning Pilot to Flight...")
    
    def remove_pilot_from_flight(self):
        print("Removing Pilot from Flight...")
    
    def get_pilot_schedule(self):
        self.pilots.get_pilot_schedule()
    
    def go_back_to_main_menu(self):
        print("Returning to Main Menu...")
        self.handle_main_menu()

    def exit_program(self):
        print("Exiting program...")
        self.db_operations.close()
        exit()
