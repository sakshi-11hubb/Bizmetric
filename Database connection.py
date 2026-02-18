import pyodbc
import sys

# DATABASE CONNECTION CLASS
class DatabaseConnection:

    def __init__(self):
        try: 
            self.conn = pyodbc.connect(
                'Driver={ODBC Driver 17 for SQL Server};'
                'Server=SAKSHI\\SQLEXPRESS01;'
                'Database=HotelDB;'
                'Trusted_Connection=yes;'
            )
            self.cursor = self.conn.cursor()

        except:
            print("Connection Error:", sys.exc_info())

# MENU CLASS
class Menu(DatabaseConnection):

    def show_menu(self):

        print("\n------ HOTEL MENU ------")

        self.cursor.execute("SELECT * FROM Menu")

        for row in self.cursor:
            print(row)            




# ORDER CLASS
class Order(DatabaseConnection):

    def __init__(self):
        super().__init__()
        self.bill = []

    def take_order(self):

        while True:

            item_id = int(input("\nEnter Item ID: "))
            quantity = int(input("Enter Quantity: "))

            # Fetch item from Menu table
            self.cursor.execute(
                "SELECT item_name, price FROM Menu WHERE id=?",
                item_id
            )

            row = self.cursor.fetchone()

            if row:

                item_name = row.item_name
                price = row.price
                total = price * quantity
                self.bill.append((item_name, price, quantity, total))
                self.cursor.execute(
                    "INSERT INTO Orders(item_name, quantity, price, total) VALUES (?,?,?,?)",
                    item_name, quantity, price, total
                )

                self.conn.commit()
                
            else:
                print("Invalid Item ID")

            choice = input("Add more items? (Y/N): ")

            if choice.upper() != "Y":
                break

   
    def print_bill(self):

        from datetime import datetime

        # get current date and time
        now = datetime.now()
        date_str = now.strftime("%d-%m-%Y")
        time_str = now.strftime("%I:%M:%S %p")

        print("\n" + "_" * 55)
        print("|" + " Welcome to Hotel Garwa ".center(53) + "|")
        print("|" + "_" * 53 + "|")

        # print date and time
        print("| Date : {0:<45}|".format(date_str))
        print("| Time : {0:<45}|".format(time_str))
        print("|" + "-" * 53 + "|")
        print("| {0:<3} {1:<15} {2:>15} {3:>15} |".format("Sr", "Menu", "Quantity", "Price"))
        print("|" + "-" * 53 + "|")

        grand_total = 0

        for index, item in enumerate(self.bill, start=1):
            name = item[0]
            price = item[1]
            qty = item[2]
            total = item[3]

            grand_total += total

            print("| {0:<3} {1:<15} {2:>15} {3:>15} |"
                .format(index, name, qty, total))

        print("|" + "_" * 53 + "|")
        print("| {0:<40} {1:>10} |".format("Total", grand_total))
        print("|" + "_" * 53 + "|")



menu = Menu()
menu.show_menu()

order = Order()
order.take_order()
print_bill_choice=input("Do you want to print bill?").upper()
if print_bill_choice=="Y":
 order.print_bill()            