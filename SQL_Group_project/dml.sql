--get all Athletes information for the athletes page
SELECT * FROM Athletes;

--get information about an athlete inputs from Athletes Page
SELECT * FROM Athletes WHERE fname = :name_selected_from_athletes_page;

--add an athlete  inputs from Athletes Page
INSERT INTO Athletes (firstName, lastName, DOB, startWeight, currentWeight, email, phone)
VALUES (:firstNameInput, :lastNameInput, :DOBInput, :startWeightInput, :currentWeightInput, :emailInput, :phoneInput);

--get all trainers information for the trainers page
SELECT * FROM Trainers;

--add a trainer inputs from trainers page
INSERT INTO Trainers (firstName, lastName, CERT, CPR,  email, phone)
VALUES (
:firstNameInput, 
:lastNameInput, 
:CERTInput, 
:CPRInput, 
:currentWeightInput, 
:emailInput, 
:phoneInput
);

--get all exercises inputs from Exercises Page
SELECT * FROM Exercises;

--add a new exercise inputs from Exercises Page
INSERT INTO Exercises (name, musclePrimary, muscleSecondary)
VALUES (:nameInput, :PrimaryMuscleInput, :SecondaryMuscleInput);

--delete an exercise inputs from Exercises Page
DELETE FROM Exercise WHERE name = :nameinput_fromExercisesPage;

--update an exercise inputs from Exercise Page
UPDATE exercise SET name = :nameInput, musclePrimary= :Primary_Muscle_groupInput, muscleSecondary = :Secondary_Muslce_Group WHERE id= :Exercise_ID_from_the_update_form;

--add a workout inputs from the Add Workout Overview form on Workouts Page
INSERT INTO Workouts (musclePrimary, muscleSecondary, duration, exercise1, exercise2, exercise3, exercise4, exercise5, exercise6, athleteID)
VALUES (
:PrimaryMuscleInput,
:SecondaryMuscleInput,
:DurationInput, 
:exercise1Input, 
:exercise2Input, 
:exercise3Input, 
:exercise4Input, 
:exercise5Input, 
:exercise6Input, 
(SELECT athleteID FROM Athletes WHERE fname = :inputFromDropdown)
);

--get all athlete's names for the dropdown menu
SELECT fname FROM Athletes;

--get all workout's details
SELECT * FROM Workouts_has_Exercises;

--add to  workout details
INSERT INTO Workouts_has_Exercises(exerciseID, workoutID, weight, reps)
VALUES (
(SELECT exerciseID FROM Exercises WHERE name = :Exercise_dropdown),
:workoutID_dropdown,
:weight_input
:reps_input
);

--get all workout id's to go into the drop down menu
SELECT workoutID FROM Workouts;

--get all exercise names to go into the drop down menu
SELECT name FROM Exercises;