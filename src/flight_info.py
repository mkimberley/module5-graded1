from db_operations import DBOperations
from tabulate import tabulate

class FlightInfo:

  def __init__(self, db_filename):
    self.db_ops = DBOperations(db_filename)
    self.db_ops.connect()


  def set_flight_id(self, flightID):
    self.flightID = flightID

  def set_flight_origin(self, flightOrigin):
    self.flight_origin = flightOrigin

  def set_flight_destination(self, flightDestination):
    self.flight_destination = flightDestination

  def set_status(self, status):
    self.status = status

  def get_flight_id(self):
    return self.flightID

  def get_flight_origin(self):
    return self.flightOrigin

  def get_airport_name(self, airportId):
    pass
  

  def get_status(self):
    return self.status

  def __str__(self):
    return str(
      self.flightID
    ) + "\n" + self.flightOrigin + "\n" + self.flightDestination + "\n" + str(
      self.status)
  
  def create_flight(self):
    try:
        print("Creating a new flight...")
        flight_number = input("Enter flight number: ")
        departure_airport_id = input("Enter departure airport ID: ")
        arrival_airport_id = input("Enter arrival airport ID: ")
        departure_time = input("Enter departure time (YYYY-MM-DD HH:MM:SS): ")
        arrival_time = input("Enter arrival time (YYYY-MM-DD HH:MM:SS): ")
        aircraft_id = input("Enter aircraft ID: ")
        status = input("Enter flight status: ")

        validations = [
            {"table": "airports", "column": "airport_id", "value": departure_airport_id, "validation_type": "existing"},
            {"table": "airports", "column": "airport_id", "value": arrival_airport_id, "validation_type": "existing"},
            {"table": "aircraft", "column": "aircraft_id", "value": aircraft_id, "validation_type": "existing"},
            {"table": "flights", "column": "flight_number", "value": flight_number, "validation_type": "unique"},
        ]
        self.db_ops.validate_fields(validations)

        query = """INSERT INTO flights (flight_number, departure_airport_id, arrival_airport_id, 
                            departure_time, arrival_time, aircraft_id, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?);"""
        
        params = (flight_number, departure_airport_id, arrival_airport_id,
                  departure_time, arrival_time, aircraft_id, status)

        self.db_ops.execute_query(query, params)  # Use DBOperations to execute query
        print("Flight created successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except sqlite3.IntegrityError as e:
        print(f"Database error: {e}")

  def update_flight_information(self):
    try:
        flight_number = input("Enter the Flight Number to update: ")
        if not self.db_ops.check_validation("flights", "flight_number", flight_number):
            print(f"Flight ID {flight_number} does not exist.")
            return

        fields_to_update = {
            "flight_number": input("Enter new flight number (leave blank to keep current): "),
            "departure_airport_id": input("Enter new departure airport ID (leave blank to keep current): "),
            "arrival_airport_id": input("Enter new arrival airport ID (leave blank to keep current): "),
            "departure_time": input("Enter new departure time (YYYY-MM-DD HH:MM:SS, leave blank to keep current): "),
            "arrival_time": input("Enter new arrival time (YYYY-MM-DD HH:MM:SS, leave blank to keep current): "),
            "aircraft_id": input("Enter new aircraft ID (leave blank to keep current): "),
            "status": input("Enter new flight status (leave blank to keep current): "),
        }

        updates, params = self._prepare_updates(fields_to_update)
        if not updates:
            print("No fields to update.")
            return

        params.append(flight_number)  # Add flight_id for the WHERE clause
        update_query = f"UPDATE flights SET {', '.join(updates)} WHERE flight_number = ?;"

        self.db_ops.execute_query(update_query, tuple(params))
        print(f"Flight {flight_number} updated successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

  def _prepare_updates(self, fields_to_update):
    """
    Helper function to prepare updates and parameters for SQL queries.
    :param fields_to_update: Dictionary of fields and their new values.
    :return: Tuple of updates and parameters.
    """
    updates = []
    params = []
    for field, value in fields_to_update.items():
        if value:
            updates.append(f"{field} = ?")
            params.append(value)
    return updates, params

  def view_flights_by_criteria(self):
    criteria_menu = [
        {"option": 1, "description": "By Flight ID", "column": "flights.flight_id"},
        {"option": 2, "description": "By Aircraft Registration", "column": "aircraft.registration_number"},
        {"option": 3, "description": "By Destination Airport", "column": "arrival_airport.airport_name"},
        {"option": 4, "description": "By Departure Airport", "column": "departure_airport.airport_name"},
        {"option": 5, "description": "By Status", "column": "flights.status"},
        {"option": 6, "description": "By Departure Time", "column": "flights.departure_time"},
        {"option": 7, "description": "By Arrival Time", "column": "flights.arrival_time"},
        {"option": 8, "description": "By Flight Number", "column": "flights.flight_number"},
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
            flights.flight_id,
            flights.flight_number,
            departure_airport.airport_name AS departure_airport_name,
            arrival_airport.airport_name AS arrival_airport_name,
            flights.departure_time,
            flights.arrival_time,
            flights.status,
            aircraft.model AS aircraft_model,
            aircraft.registration_number AS aircraft_registration
        FROM 
            flights
        JOIN 
            airports AS departure_airport ON flights.departure_airport_id = departure_airport.airport_id
        JOIN 
            airports AS arrival_airport ON flights.arrival_airport_id = arrival_airport.airport_id
        JOIN 
            aircraft ON flights.aircraft_id = aircraft.aircraft_id
        WHERE 
            {selected_criteria['column']} = ?;
        """

        results = self.db_ops.execute_query(query, (search_value,))  # Use DBOperations to execute query

        if results:
            headers = [
                "Flight ID", "Flight Number", "Departure Airport", "Arrival Airport",
                "Departure Time", "Arrival Time", "Status", "Aircraft Model", "Aircraft Registration"
            ]
            table = tabulate(results, headers=headers, tablefmt="grid")
            print(table)
        else:
            print("No flights found matching the given criteria.")
    except ValueError:
        print("Invalid input. Please enter a number.")
