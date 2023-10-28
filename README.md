# Weerawat-T.-
Assignment at Lincoln uni 
## Motorkhana Report

1. Structure of the Solution
Routes & Functions
* Homepage ("/")
    * Function: home()
    * Description: Displays the base page of the application.
* Junior Drivers ("/juniordrivers")
    * Function: juniordrivers()
    * Description: Lists junior drivers and fetches details like their first name, surname, date of birth, and caregiver's name.
* Search Driver ("/searchdriver")
    * Function: searchdriver()
    * Description: Provides an interface for searching drivers by their first name or surname.
* Add Driver ("/adddriver")
    * Function: adddriver()
    * Description: Interface to add new drivers with details like first name, surname, date of birth, age, junior status, caregiver ID, and car.
* List Drivers ("/listdrivers")
    * Function: listdrivers()
    * Description: Lists all drivers with details like first name, surname, date of birth, age, car model, and drive class.
* Driver Details ("/driver/<int:driver_id>")
    * Function: driver_details(driver_id)
    * Description: Displays specific driver details based on driver ID.
* List Courses ("/listcourses")
    * Function: listcourses()
    * Description: Lists all available courses.
* Show Graph ("/graph")
    * Function: showgraph()
    * Description: Provides a graphical representation of the top 5 drivers based on the number of completed courses.

2. Assumptions & Design Decisions
Assumptions
* 		Driver-Caregiver Relationship: The system assumes a left join between drivers and caregivers, meaning that not every junior driver may have an associated caregiver.
* 		Search Mechanism: The driver search mechanism assumes a simple name-based search, and does not consider other parameters like age or car number.
* 		Car-Driver Association: The application assumes a one-to-one relationship between the car and the driver, signified by a left join operation.
Design Decisions
* Database Connection: The application employs the mysql.connector library for establishing a connection with the database, and a separate getCursor function was designed for streamlined access to database operations.
* Data Storage and Retrieval: Predominantly, SQL JOIN operations were employed for efficient data fetch operations. For instance, the listdrivers route fetches the driver's car details using a left join.
* Driver Classification: Junior drivers are identified using the is_junior attribute, and their details, along with their caregiver's details, are retrieved accordingly.
* Search Mechanism Enhancement: The search mechanism has been enhanced to accommodate both first names and surnames using the LIKE SQL clause, improving the search scope.
* Graph Data Extraction: For the graphical representation, only the top 5 drivers are considered based on the number of courses they completed.

## Database Questions **
1. What SQL statement creates the car table and defines its three fields/columns? (Copy and paste the relevant lines of SQL.)** ```sql CREATE TABLE IF NOT EXISTS car ( car_num INT PRIMARY KEY NOT NULL, model VARCHAR(20) NOT NULL, drive_class VARCHAR(3) NOT NULL );

2. Which line of SQL code sets up the relationship between the car and driver tables?

Copy code
FOREIGN KEY (car) REFERENCES car(car_num) ON UPDATE CASCADE ON DELETE CASCADE

3. Which 3 lines of SQL code insert the Mini and GR Yaris details into the car table?


Copy code
INSERT INTO car VALUES (11,'Mini','FWD'), (17,'GR Yaris','4WD');

4. Suppose the club wanted to set a default value of ‘RWD’ for the driver_class field. What specific change would you need to make to the SQL to do this? (Do not implement this change in your app.)


Copy code
drive_class VARCHAR(3) NOT NULL DEFAULT 'RWD'


5.Suppose logins were implemented. Why is it important for drivers and the club admin to access different routes? As part of your answer, give two specific examples of problems that could occur if all of the web app facilities were available to everyone.

Importance: Separating access makes sure that only the right people can change the system or see private details. This keeps the data safe and stops bad or mistaken changes.


