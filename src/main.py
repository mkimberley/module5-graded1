# main.py
import logging
from db_operations import DBOperations
from db_initialise import initialise_database
from greet import Greet

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("squeezyjet.log"),
        logging.StreamHandler()
    ]
)

db_filename = "FlightDB.db"

def main():
    initialise_database(db_filename)

    
    greeter = Greet()
    greeter.greet()  
    
    while True:
        print("\n Menu:")
        print("**********")
        print(" 1. Create table FlightInfo")
        print(" 2. Insert data into FlightInfo")
        print(" 3. Select all data from FlightInfo")
        print(" 4. Search a flight")
        print(" 5. Update data some records")
        print(" 6. Delete data some records")
        print(" 7. Exit\n")

        __choose_menu = int(input("Enter your choice: "))
        db_ops = DBOperations(db_filename)
        db_ops.connect()
        if __choose_menu == 1:
            db_ops.create_table()
        elif __choose_menu == 2:
            db_ops.insert_data()
        elif __choose_menu == 3:
            db_ops.select_all()
        elif __choose_menu == 4:
            db_ops.search_data()
        elif __choose_menu == 5:
            db_ops.update_data()
        elif __choose_menu == 6:
            db_ops.delete_data()
        elif __choose_menu == 7:
            db_ops.close()
            exit(0)
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()