from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

# Configuration
# Citation for the following program:
# Date: 07/24/2022
# Most of the setup and examples for mySQL statements came from the first exercise. That had a walkthrough listed below.
# 1- Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_'
app.config['MYSQL_PASSWORD'] = ''  # last 4 of onid
app.config['MYSQL_DB'] = 'cs340_'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)


# Routes

@app.route('/')
def root():
    return render_template("main.j2")


# Citation for the following function: Date: 07/24/2022 Line 54 was not working with the typical formatting in the
# second source listed below so I had to use an alternative method 1- Source URL:
# https://stackoverflow.com/questions/21740359/python-mysqldb-typeerror-not-all-arguments-converted-during-string
# -formatting 2- Source URL: https://stackoverflow.com/questions/35172967/python-flask-insert-data-into-mysql
@app.route('/athletes', methods=['GET', 'POST'])
def athletes():
    if request.method == "GET":
        query = 'SELECT * from Athletes'
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()
        return render_template("athletes.j2", athletes=results)
    if request.method == "POST":
        if request.form.get('addAthlete') == 'Add Athlete':
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            DOB = request.form["DOB"]
            startWeight = request.form["startWeight"]
            currentWeight = request.form["currentWeight"]
            email = request.form["email"]
            phone = request.form["phone"]
            insert = 'INSERT INTO Athletes (firstName, lastName, DOB, startWeight, currentWeight, email, phone) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            curPost = mysql.connection.cursor()
            curPost.execute(insert, (firstName, lastName, DOB, startWeight, currentWeight, email, phone))
            mysql.connection.commit()
            return redirect("/athletes")
        if request.form.get('searchAthlete') == 'Search Athlete':
            searchType = "Athletes"
            tableHeader = ["First Name", "Last Name", "DOB", "Start Weight", "Current Weight", "Email", "Phone"]
            searchName = request.form["search_name"]
            curSearch = mysql.connection.cursor()
            curSearch.execute("SELECT * FROM Athletes WHERE firstName = %s", [searchName])
            searchResults = curSearch.fetchall()
            return render_template("search.j2", type=searchName, headers=tableHeader, results=searchResults)


# Citation for the following function:
# Date: 07/24/2022
# I recieved a 405 method not allowed error for this function.  The below source fixed that.
# 1- Source URL: https://stackoverflow.com/questions/21689364/method-not-allowed-flask-error-405
@app.route('/trainers', methods=['GET', 'POST'])
def trainers():
    if request.method == "GET":
        query = 'SELECT * FROM Trainers'
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()
        return render_template("trainers.j2", trainers=results)
    if request.method == "POST":
        if request.form.get('addTrainer') == 'Add Trainer':
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            CERT = request.form["CERT"]
            CPR = request.form["CPR"]
            email = request.form["email"]
            phone = request.form["phone"]
            insert = 'INSERT INTO Trainers (firstName, lastName, CERT, CPR, email, phone) VALUES (%s, %s, %s, %s, %s, %s)'
            curPost = mysql.connection.cursor()
            curPost.execute(insert, (firstName, lastName, CERT, CPR, email, phone))
            mysql.connection.commit()
            return redirect("/trainers")


# Citation for the following function:
# Date: 07/24/2022
# I struggled with figuring out out to combine the exerciseID with the name.  The below source helped with that.
# 1- Source URL: https://stackoverflow.com/questions/71465165/how-to-retrieve-a-value-from-html-form-and-use-that-value-inside-the-sql-query-i
@app.route('/exercises', methods=['GET', 'POST'])
def exercises():
    if request.method == "GET":
        query = 'SELECT * FROM Exercises'
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()
        return render_template("exercises.j2", exercises=results)
    if request.method == "POST":
        if request.form.get('addExercise') == 'Add Exercise':
            name = request.form["name"]
            muscle_group = request.form["muscle_group"]
            secondary_muscle = request.form["secondary_muscle"]
            insert = 'INSERT INTO Exercises (name, muscle_group, secondary_muscle) VALUES (%s, %s, %s)'
            curPost = mysql.connection.cursor()
            curPost.execute(insert, (name, muscle_group, secondary_muscle))
            mysql.connection.commit()
            return redirect("/exercises")
        if request.form.get('deleteExercise') == 'Delete Exercise':
            name = request.form["name"]
            curDelete = mysql.connection.cursor()
            curDelete.execute("DELETE FROM Exercises WHERE name = %s", [name])
            mysql.connection.commit()
            return redirect("/exercises")
        if request.form.get('updateExercise') == 'Update Exercise':
            exerciseID = request.form["exerciseID"]
            name = request.form["name"]
            muscle_group = request.form["muscle_group"]
            secondary_muscle = request.form["secondary_muscle"]
            if name and muscle_group and secondary_muscle:
                update = "UPDATE Exercises SET name = %s, muscle_group = %s, secondary_muscle = %s where exerciseID = %s"
                curUpdate = mysql.connection.cursor()
                curUpdate.execute(update, (name, muscle_group, secondary_muscle, exerciseID))
                mysql.connection.commit()
            if name and muscle_group:
                update = "UPDATE Exercises SET name = %s, muscle_group = %s where exerciseID = %s"
                curUpdate = mysql.connection.cursor()
                curUpdate.execute(update, (name, muscle_group, exerciseID))
                mysql.connection.commit()
            if name and secondary_muscle:
                update = "UPDATE Exercises SET name = %s, secondary_muscle = %s where exerciseID = %s"
                curUpdate = mysql.connection.cursor()
                curUpdate.execute(update, (name, secondary_muscle, exerciseID))
                mysql.connection.commit()
            if name:
                update = "UPDATE Exercises SET name = %s where exerciseID = %s"
                curUpdate = mysql.connection.cursor()
                curUpdate.execute(update, (name, exerciseID))
                mysql.connection.commit()
            if muscle_group and secondary_muscle:
                update = "UPDATE Exercises SET muscle_group = %s, secondary_muscle = %s where exerciseID = %s"
                curUpdate = mysql.connection.cursor()
                curUpdate.execute(update, (muscle_group, secondary_muscle, exerciseID))
                mysql.connection.commit()
            if muscle_group:
                update = "UPDATE Exercises SET muscle_group = %s where exerciseID = %s"
                curUpdate = mysql.connection.cursor()
                curUpdate.execute(update, (muscle_group, exerciseID))
                mysql.connection.commit()
            if secondary_muscle:
                update = "UPDATE Exercises SET secondary_muscle = %s where exerciseID = %s"
                curUpdate = mysql.connection.cursor()
                curUpdate.execute(update, (secondary_muscle, exerciseID))
                mysql.connection.commit()
            return redirect("/exercises")

        # No sources required here.  Mostly repeated code from above.


@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    if request.method == "GET":
        query = 'SELECT * FROM Workouts'
        cur = mysql.connection.cursor()
        cur.execute(query)
        workoutOverview = cur.fetchall()

        query = 'SELECT * FROM Workouts_has_Exercises'
        cur = mysql.connection.cursor()
        cur.execute(query)
        workoutDetails = cur.fetchall()

        query = 'SELECT exerciseID, name FROM Exercises'
        cur = mysql.connection.cursor()
        cur.execute(query)
        exerciseNameDropdown = cur.fetchall()

        query = 'SELECT athleteID, firstName, lastName FROM Athletes'
        cur = mysql.connection.cursor()
        cur.execute(query)
        athleteDropdown = cur.fetchall()
        return render_template("workouts.j2", workouts=workoutOverview, workoutdetails=workoutDetails,
                               exercises=exerciseNameDropdown, athletes=athleteDropdown)
    if request.method == "POST":
        if request.form.get('addWorkoutSummary') == 'Add Workout Summary':
            musclePrimary = request.form["musclePrimary"]
            muscleSecondary = request.form["muscleSecondary"]
            duration = request.form["duration"]
            exercise1 = request.form["exercise1"]
            exercise2 = request.form["exercise2"]
            exercise3 = request.form["exercise3"]
            exercise4 = request.form["exercise4"]
            exercise5 = request.form["exercise5"]
            exercise6 = request.form["exercise6"]
            athleteID = request.form["athlete"]
            insert = 'INSERT INTO Workouts (musclePrimary, muscleSecondary, duration, exercise1, exercise2, exercise3, exercise4, exercise5, exercise6, athleteID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            curPost = mysql.connection.cursor()
            curPost.execute(insert, (
            musclePrimary, muscleSecondary, duration, exercise1, exercise2, exercise3, exercise4, exercise5, exercise6,
            athleteID))
            mysql.connection.commit()
            return redirect("/workouts")
        if request.form.get('addWorkoutDetails') == 'Add Workout Details':
            workoutID = request.form["workoutID"]
            exerciseID = request.form["exerciseID"]
            weight = request.form["weight"]
            reps = request.form["reps"]
            insert = 'INSERT INTO Workouts_has_Exercises (workoutID, exerciseID, weight, reps) VALUES (%s, %s, %s, %s)'
            curPost = mysql.connection.cursor()
            curPost.execute(insert, (workoutID, exerciseID, weight, reps))
            mysql.connection.commit()
            return redirect("/workouts")


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9493))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=True)
