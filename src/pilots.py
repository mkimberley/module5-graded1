from db_operations import DBOperations
from tabulate import tabulate

class Pilots:

    def __init__(self, db_filename):
        self.db_ops = DBOperations(db_filename)
        self.db_ops.connect()

    def view_pilot(self):
        criteria_menu = [
            {"option": 1, "description": "By Pilot ID", "column": "pilot.pilot_id"},
            {"option": 2, "description": "By Pilot First Name", "column": "pilot.first_name"},
            {"option": 3, "description": "By Pilot Last Name", "column": "pilot.last_name"},
            {"option": 4, "description": "By Pilot License Number", "column": "pilot.license_number"},

        ]
        print("\nSearch Criteria:")
        print("****************")
        for item in criteria_menu:
            print(f" {item['option']}. {item['description']}")
        print("\n")

        try:
            choice = int(input("Enter your choice: "))
            selected_criteria = next((item for item in criteria_menu if item["option"] == choice), None)
            if not selected_criteria:
                print("Invalid choice. Please try again.")
                return

            search_value = input(f"Enter value for {selected_criteria['description']}: ")
            query = f"""
            SELECT             
                pilot.pilot_id,
                pilot.first_name,
                pilot.last_name,
                pilot.license_number,
                pilot.contact_info
            FROM 
                pilot
            WHERE 
                {selected_criteria['column']} = ?;
            """

            results = self.db_ops.execute_query(query, (search_value,))  # Use DBOperations to execute query

            if results:
                headers = [
                    "Pilot ID", "First Name", "Last Name", "License Number", "Contact Info"
                ]
                table = tabulate(results, headers=headers, tablefmt="grid")
                print(table)
            else:
                print("No pilots found matching the given criteria.")
        except ValueError:
            print("Invalid input. Please enter a number.")


    def add_pilot(self):
        print("Adding Pilot...")
        first_name = input("Enter Pilot's First Name: ")
        last_name = input("Enter Pilot's Last Name: ")
        license_number = input("Enter Pilot's License Number: ")
        contact_info = input("Enter Pilot's Contact Information: ")

        query = """
        INSERT INTO pilot (first_name, last_name, license_number, contact_info)
        VALUES (?, ?, ?, ?);
        """
        self.db_ops.execute_query(query, (first_name, last_name, license_number, contact_info))
        print("Pilot added successfully.")
    
    def update_pilot_information(self):
        return
    
    def assign_pilot_to_flight(self):
        return
    
    def remove_pilot_from_flight(self):
        return
    
    def get_pilot_schedule(self):
        criteria_menu = [
            {"option": 1, "description": "By Pilot ID", "column": "pilot.pilot_id"},

        ]
        print("\nSearch Criteria:")
        print("****************")
        for item in criteria_menu:
            print(f" {item['option']}. {item['description']}")
        print("\n")

        try:
            choice = int(input("Enter your choice: "))
            selected_criteria = next((item for item in criteria_menu if item["option"] == choice), None)
            if not selected_criteria:
                print("Invalid choice. Please try again.")
                return

            search_value = input(f"Enter value for {selected_criteria['description']}: ")
            query = """
                    SELECT 
                        flights.flight_id,
                        flights.flight_number,
                        departure_airport.airport_name AS departure_airport_name,
                        arrival_airport.airport_name AS arrival_airport_name,
                        flights.departure_time,
                        flights.arrival_time,
                        flights.status AS flight_status,
                        aircraft.model AS aircraft_model,
                        aircraft.registration_number AS aircraft_registration,
                        pilot.pilot_id,
                        pilot.first_name AS pilot_first_name,
                        pilot.last_name AS pilot_last_name,
                        pilot.license_number AS pilot_license_number
                    FROM 
                        flight_pilot
                    JOIN 
                        flights ON flight_pilot.flight_id = flights.flight_id
                    JOIN 
                        airports AS departure_airport ON flights.departure_airport_id = departure_airport.airport_id
                    JOIN 
                        airports AS arrival_airport ON flights.arrival_airport_id = arrival_airport.airport_id
                    JOIN 
                        aircraft ON flights.aircraft_id = aircraft.aircraft_id
                    JOIN 
                        pilot ON flight_pilot.pilot_id = pilot.pilot_id
                    WHERE 
                        flight_pilot.pilot_id = ?;
                    """

            results = self.db_ops.execute_query(query, (search_value,))  # Use DBOperations to execute query

            if results:
                headers = [
                    "Flight ID", "Flight Number", "Departure Airport", "Arrival Airport",
                    "Departure Time", "Arrival Time", "Flight Status", "Aircraft Model",
                    "Aircraft Registration", "Pilot ID", "Pilot Name", "Pilot Surname", "License Number", "Contact Info"
                ]
                table = tabulate(results, headers=headers, tablefmt="grid")
                print(table)
            else:
                print("No pilots found matching the given criteria.")
        except ValueError:
            print("Invalid input. Please enter a number.")

