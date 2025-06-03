from db_operations import DBOperations
from tabulate import tabulate

class FlightInfo:

  def __init__(self, db_filename):
    self.flightID = 0
    self.flightOrigin = ''
    self.flightDestination = ''
    self.status = ''
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
    # Placeholder implementation
    pass


  def get_status(self):
    return self.status

  def __str__(self):
    return str(
      self.flightID
    ) + "\n" + self.flightOrigin + "\n" + self.flightDestination + "\n" + str(
      self.status)

  def view_flights_by_criteria(self):
    criteria_menu = [
        {"option": 1, "description": "By Flight ID", "column": "flights.flight_id"},
        {"option": 2, "description": "By Aircraft Registration", "column": "aircraft.registration_number"},
        {"option": 3, "description": "By Destination Airport", "column": "arrival_airport.airport_name"},
        {"option": 4, "description": "By Departure Airport", "column": "departure_airport.airport_name"},
        {"option": 5, "description": "By Status", "column": "flights.status"},
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
