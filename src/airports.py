from db_operations import DBOperations
from tabulate import tabulate

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