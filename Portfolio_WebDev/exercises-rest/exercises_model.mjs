import mongoose from 'mongoose';
import 'dotenv/config';
import { query } from 'express';

mongoose.connect(
    process.env.MONGODB_CONNECT_STRING,
    { useNewUrlParser: true }
);
/**
*
* @param {string} date
* Return true if the date format is MM-DD-YY where MM, DD and YY are 2 digit integers
*/
function isDateValid(date) {
    // Test using a regular expression. 
    // To learn about regular expressions see Chapter 6 of the text book
    const format = /^\d\d-\d\d-\d\d$/;
    return format.test(date);
}

const db = mongoose.connection;

const exerciseSchema = mongoose.Schema({
    name: { type: String, required: true },
    reps: { type: Number, required: true },
    weight: {type: Number, required: true },
    unit: {type: String, required: true},
    date: {type: String, required: true}
});

const Exercise = mongoose.model("Exercise", exerciseSchema)

const createExercise = async (name, reps, weight, unit, date) => {
    if(name.length < 1){
        throw error
    }
    if(isDateValid(date) !== true){
        throw error
    }
    if(Number.isInteger(parseInt(reps)) !== true || reps < 1){
        throw error
    }
    if(Number.isInteger(parseInt(weight)) !== true || weight < 1){
        throw error
    }
    if(unit !== "kgs"){
        if(unit !== "lbs"){
            throw error
        }
    }
    const ex = new Exercise({ name: name , reps: reps, weight: weight, unit: unit, date: date});
    return ex.save();
}

const findEx = async (filter) => {
    const query = Exercise.find(filter);
    return query.exec();
}

const findExById = async (_id) => {
    const query = Exercise.findById(_id);
    return query.exec();
}

const updateEx = async (_id, name, reps, weight, unit, date) => {
    if(name.length < 1){
        throw error
    }
    if(isDateValid(date) !== true){
        throw error
    }
    if(Number.isInteger(parseInt(reps)) !== true || reps < 1){
        throw error
    }
    if(Number.isInteger(parseInt(weight)) !== true || weight < 1){
        throw error
    }
    if(unit !== "kgs"){
        if(unit !== "lbs"){
            throw error
        }
    }
    const result = await Exercise.updateOne({_id: _id}, {name: name, reps: reps, weight: weight, unit: unit, date: date});
    console.log(result.modifiedCount)
    return result.modifiedCount;
}

const deleteById = async (_id) => {
    const result = await Exercise.deleteMany({ _id });
    return result.deletedCount;
}

db.once("open", () => {
    console.log("Successfully connected to MongoDB using Mongoose!");
});


export { createExercise, findEx, updateEx, deleteById, findExById };