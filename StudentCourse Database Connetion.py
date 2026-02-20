import pyodbc
import sys

# DATABASE CONNECTION 
class DatabaseConnection:

    def __init__(self):
        try:
            self.conn = pyodbc.connect(
                'Driver={ODBC Driver 17 for SQL Server};'
                'Server=SAKSHI\\SQLEXPRESS01;'
                'Database=CollegeDB;'
                'Trusted_Connection=yes;'
            )
            self.cursor = self.conn.cursor()

        except:
            print("Connection Error:", sys.exc_info())


#  COURSE CLASS 

class Course(DatabaseConnection):

    def __init__(self):
        super().__init__()

        self.subjects = ["HR", "Finance", "Marketing", "DS"]
        self.core_fee = 200000
        self.analytics_extra = 0.10 * self.core_fee   

    def calculate_total(self):

        print("\nAvailable Courses:", self.subjects)

        subject = input("Enter Subject: ")
        analytics = input("Analytics (Y/N): ").upper()
        hostel = input("Hostel (Y/N): ").upper()
        food_months = int(input("Food for how many months?: "))
        transport = input("Transportation (semester/annual): ").lower()

        total = 0

        # Core Fee 
        total += self.core_fee

        # Analytics Condition 
        if subject in ["HR", "Finance", "Marketing"]:
            if analytics == "Y":
                total += self.analytics_extra
        else:
            print("Analytics not available for DS")

        #Hostel 
        if hostel == "Y":
            total += 200000  

        # Food 
        total += food_months * 2000

        #transport
        if transport == "semester":
            total += 13000 * 2   
        elif transport == "annual":
            total += 13000

        print("\nTotal Annual Cost =", total)

        self.cursor.execute("""
            INSERT INTO StudentCourse
            (subject, analytics, hostel, food_months, transportation, total_cost)
            VALUES (?,?,?,?,?,?)
        """,
        subject, analytics, hostel, food_months, transport, total)

        self.conn.commit()
        print("Data Saved Successfully!")
 

course = Course()
course.calculate_total()