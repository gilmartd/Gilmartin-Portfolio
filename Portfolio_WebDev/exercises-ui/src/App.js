import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import CreateExercisePage from './pages/CreateExercisePage';
import EditExercisePage from './pages/EditExercisePage';

import { useState } from 'react';

<header>
  <h1> Exercise UI App</h1>
  <p> This application is a portfolio assignment for CS 290: Web Development. The app focuses on CRUD operations for a react app, using express and MongoDB.</p>
</header>

function App() {
  const [exerciseToEdit, setExerciseToEdit] = useState();
  return (
    <div className="App">
      <header>
        <h1> Exercise UI App</h1>
        <p> This application is a portfolio assignment for CS 290, web development class. The app focuses on CRUD operations for a react app, using express and MongoDB.</p>
      </header>

      <Router>
        <div className="App-header">
        <nav>
          <Link to="/" id = "addnew">Home</Link>
          <Link to="/add-exercise" id = "addnew">Add New</Link>
         </nav>
          <Route path="/" exact>
            <HomePage setExerciseToEdit={setExerciseToEdit} />
          </Route>
          <Route path="/add-exercise">
            <CreateExercisePage />
          </Route>
          <Route path="/edit-exercise">
            <EditExercisePage exerciseToEdit={exerciseToEdit} />
          </Route>
        </div>
      </Router>
      <footer> ©2022 Derek Gilmartin </footer>
    </div>
  );
}

export default App;