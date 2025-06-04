from db_operations import DBOperations
from tabulate import tabulate
from common import Common

class Airports:

    def __init__(self, db_filename):
        self.db_ops = DBOperations(db_filename)
        self.db_ops.connect()

    def view_airports(self):
        query = """
        SELECT 
            airport_id, 
            airport_code, 
            airport_name, 
            city, 
            country 
        FROM 
            airports;
        """
        results = self.db_ops.execute_query(query)

        if results:
            headers = ["Airport ID", "Airport Code", "Airport Name", "City", "Country"]
            table = tabulate(results, headers=headers, tablefmt="grid")
            print(table)
        else:
            print("No airports found.")

    def add_airport(self):
        airport_code = input("Enter Airport Code: ")
        airport_name = input("Enter Airport Name: ")
        city = input("Enter City: ")
        country = input("Enter Country: ")

        # Basic empty field validation
        if not all([airport_code.strip(), airport_name.strip(), city.strip(), country.strip()]):
            print("All fields are required.")
            return

        validations = [
            {"table": "airports", "column": "airport_code", "value": airport_code, "validation_type": "unique"},
            {"table": "airports", "column": "airport_name", "value": airport_name, "validation_type": "unique"},
        ]
        self.db_ops.validate_fields(validations)

        query = """
        INSERT INTO airports (airport_code, airport_name, city, country)
        VALUES (?, ?, ?, ?);
        """
        params = (airport_code, airport_name, city, country)
        self.db_ops.execute_query(query, params)
        print(f"Airport {airport_name} added successfully.")
    
    def delete_airport(self):
        airport_code = input("Enter the Airport Code to delete: ")

        # Check that the airport_code exists
        exists = self.db_ops.check_validation("airports", "airport_code", airport_code)
        if not exists:
            print(f"Airport with code {airport_code} does not exist.")
            return

        # Get the airport_id for further checks
        query = "SELECT airport_id FROM airports WHERE airport_code = ?;"
        result = self.db_ops.execute_query(query, (airport_code,))
        airport_id = result.fetchone()[0] if result else None

        # Only remove the airport if no flights are associated with it
        query = """
        SELECT COUNT(*) FROM flights WHERE departure_airport_id = ? OR arrival_airport_id = ?;
        """
        count = self.db_ops.execute_query(query, (airport_id, airport_id)).fetchone()[0]
        if count > 0:
            print(f"Cannot delete airport {airport_code} as it is associated with existing flights.")
            return

        # If no flights are associated, proceed to delete the airport
        query = "DELETE FROM airports WHERE airport_code = ?;"
        self.db_ops.execute_query(query, (airport_code,))
        print(f"Airport with code {airport_code} deleted successfully.")