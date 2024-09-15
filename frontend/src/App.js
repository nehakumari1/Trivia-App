import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'

// import logo from './logo.svg';
import './stylesheets/App.css';
import FormView from './components/FormView';
import QuestionView from './components/QuestionPage';
import Header from './components/Header';
import QuizGame from './components/QuizGame';


class App extends Component {
  render() {
    return (
    <div className="App">
      <Header path />
      <Router>
        <Switch>
          <Route path="/" exact component={QuestionPage} />
          <Route path="/add" component={FormView} />
          <Route path="/play" component={QuizGame} />
          <Route component={QuestionPage} />
        </Switch>
      </Router>
    </div>
  );

  }
}

export default App;
