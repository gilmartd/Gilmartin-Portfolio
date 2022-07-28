import 'dotenv/config';
import express from 'express';
import * as exercises from './exercises_model.mjs';

const app = express();

const PORT = process.env.PORT;

app.use(express.json());

/**
 * Create a new movie with the title, year and language provided in the body
 */

 app.post('/exercises', (req, res) => {
     const exercise = exercises.createExercise(req.body.name, req.body.reps, req.body.weight, req.body.unit, req.body.date)
        .then(ex => {
            res.status(201).json(ex);
        })
        .catch(error => {
            console.error(error);
            // In case of an error, send back status code 400 in case of an error.
            // A better approach will be to examine the error and send an
            // error status code corresponding to the error.
            res.status(400).json({ Error: 'Invalid Request' });
        });
});


/**
 * Retrieve the movie corresponding to the ID provided in the URL.
 */

app.get('/exercises/:_id', (req, res) => {
    const exId = req.params._id;
    exercises.findExById(exId)
        .then(ex => { 
            if (ex !== null) {
                res.json(ex);
            } else {
                res.status(404).json({ Error: 'Not Found' });
            }         
         })
        .catch(error => {
            res.status(400).json({ Error: 'Request failed' });
        });

});

/**
 * Retrieve movies. 
 * If the query parameters include a year, then only the movies for that year are returned.
 * Otherwise, all movies are returned.
 */

 app.get('/exercises', (req, res) => {
     let filter = {};
    exercises.findEx(filter, '', 0)
        .then(exercises => {
            res.send(exercises);
        })
        .catch(error => {
            console.error(error);
            res.send({ Error: 'Invalid Request' });
        });

});
/**
 * Update the movie whose id is provided in the path parameter and set
 * its title, year and language to the values provided in the body.
 */
 app.put('/exercises/:_id', (req, res) => {

    exercises.updateEx(req.params._id, req.body.name, req.body.reps, req.body.weight, req.body.unit, req.body.date)
        .then(numUpdated => {
            if (numUpdated === 1) {
                res.json({ _id: req.params._id, name: req.body.name, reps: req.body.reps, weight: req.body.weight, unit: req.body.unit, date: req.body.date})
            } else {
                res.status(404).json({ Error: 'Not Found' });
            }
        })
        .catch(error => {
            console.error(error);
            res.status(400).json({ Error: 'Invalid request' });
        });
});

/**
 * Delete the movie whose id is provided in the query parameters
 */
 app.delete('/exercises/:_id', (req, res) => {
    exercises.deleteById(req.params._id)
        .then(deletedCount => {
            if (deletedCount === 1) {
                res.status(204).send();
            } else {
                res.status(404).json({ Error: 'Resource not found' });
            }
        })
        .catch(error => {
            console.error(error);
            res.send({ error: 'Request failed' });
        });
});

app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
});