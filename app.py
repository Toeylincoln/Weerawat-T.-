from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/juniordrivers")
def juniordrivers():
    connection, cursor = getCursor()
    sql = """SELECT d.first_name, d.surname, d.date_of_birth, c.first_name AS caregiver_name
             FROM driver d
             LEFT JOIN caregiver c ON d.caregiver_id = c.id
             WHERE d.is_junior = 1
             ORDER BY d.age DESC, d.surname;"""
    cursor.execute(sql)
    juniors = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("juniordrivers.html", drivers=juniors)

@app.route("/searchdriver", methods=['POST', 'GET'])
def searchdriver():
    if request.method == 'POST':
        name = request.form['name']
        connection, cursor = getCursor()
        sql = """SELECT first_name, surname FROM driver 
                 WHERE first_name LIKE %s OR surname LIKE %s;"""
        cursor.execute(sql, (f"%{name}%", f"%{name}%"))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("driversearchresults.html", drivers=results)
    return render_template("searchdriver.html")

@app.route("/adddriver", methods=['POST', 'GET'])
def adddriver():
    if request.method == 'POST':
        first_name = request.form['first_name']
        surname = request.form['surname']
        date_of_birth = request.form['date_of_birth']
        age = int(request.form['age'])
        is_junior = bool(request.form['is_junior'])
        caregiver_id = int(request.form['caregiver_id'])
        car = request.form['car']

        connection, cursor = getCursor()
        sql = """INSERT INTO driver (first_name, surname, date_of_birth, age, is_junior, caregiver_id, car)
                 VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        cursor.execute(sql, (first_name, surname, date_of_birth, age, is_junior, caregiver_id, car))
        
        cursor.close()
        connection.close()
        return redirect(url_for('home'))

    connection, cursor = getCursor()
    sql = """SELECT id, first_name FROM caregiver;"""
    cursor.execute(sql)
    caregivers = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("adddriver.html", caregivers=caregivers)

@app.route("/listdrivers")
def listdrivers():
    connection, cursor = getCursor()
    sql = """SELECT d.driver_id, d.first_name, d.surname, d.date_of_birth, d.age, c.model, c.drive_class
             FROM driver d
             LEFT JOIN car c ON d.car = c.car_num
             ORDER BY d.surname, d.first_name;"""
    cursor.execute(sql)
    driverList = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("driverlist.html", driver_list = driverList)

@app.route("/driver/<int:driver_id>")
def driver_details(driver_id):
    connection, cursor = getCursor()
    sql = """SELECT d.driver_id, d.first_name, d.surname, d.date_of_birth, d.age, c.model, c.drive_class
             FROM driver d
             LEFT JOIN car c ON d.car = c.car_num
             WHERE d.driver_id = %s;"""
    cursor.execute(sql, (driver_id,))
    driver_details = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template("driver_details.html", driver=driver_details)

@app.route("/listcourses")
def listcourses():
    connection, cursor = getCursor()
    cursor.execute("SELECT * FROM course;")
    courseList = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("courselist.html", course_list = courseList)

@app.route("/graph")
def showgraph():
    connection, cursor = getCursor()
    sql = """SELECT d.driver_id, d.first_name, COUNT(c.course_id) AS completed_courses 
             FROM driver d
             JOIN course_registration cr ON d.driver_id = cr.driver_id
             JOIN course c ON cr.course_id = c.course_id
             GROUP BY d.driver_id, d.first_name
             ORDER BY completed_courses DESC
             LIMIT 5;"""
    cursor.execute(sql)
    top_drivers = cursor.fetchall()
    cursor.close()
    connection.close()
    
    # Extracting data for graph plotting
    name_list = [driver[1] for driver in top_drivers]
    value_list = [driver[2] for driver in top_drivers]
    return render_template("top5graph.html", name_list=name_list, value_list=value_list)

if __name__ == "__main__":
    app.run(debug=True)
