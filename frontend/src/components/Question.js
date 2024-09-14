import React, { Component } from 'react';
import '../stylesheets/Question.css';

class Question extends Component {
  constructor(){
    super();
    this.state = {
      isAnswerVisible: false, // Updated variable name
    };
  }

  // Toggle the visibility of the answer
  toggleAnswerVisibility() {
    this.setState((prevState) => ({
      isAnswerVisible: !prevState.isAnswerVisible
    }));
  }

  render() {
    const { question, answer, category, difficulty } = this.props;
    const { isAnswerVisible } = this.state; // Deconstruct state variable

    return (
      <div className="question-container">
        <div className="question-text">{question}</div>
        <div className="question-details">
          <img className="category-icon" src={`${category}.svg`} alt="Category" />
          <div className="difficulty-level">Difficulty: {difficulty}</div>
          <img 
            src="delete.png" 
            className="delete-icon" 
            alt="Delete" 
            onClick={() => this.props.handleQuestionAction('DELETE')}
          />
        </div>
        <div 
          className="toggle-answer button" 
          onClick={() => this.toggleAnswerVisibility()}>
          {isAnswerVisible ? 'Hide' : 'Show'} Answer
        </div>
        <div className="answer-container">
          <span style={{ visibility: isAnswerVisible ? 'visible' : 'hidden' }}>
            Answer: {answer}
          </span>
        </div>
      </div>
    );
  }
}

export default Question;
