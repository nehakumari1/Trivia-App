import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/QuizView.css';

const maxQuestionsPerGame = 5;

class QuizGame extends Component {
  constructor(props){
    super(props);
    this.state = {
      selectedCategory: null,
      pastQuestions: [],
      displayAnswer: false,
      allCategories: {},
      correctAnswersCount: 0,
      activeQuestion: {},
      userAnswer: '',
      endGame: false
    };
  }

  componentDidMount() {
    this.loadCategories();
  }

  loadCategories = () => {
    $.ajax({
      url: `/categories`,
      type: "GET",
      success: (data) => {
        this.setState({ allCategories: data.categories });
      },
      error: () => {
        alert('Failed to load categories. Please try again.');
      }
    });
  }

  chooseCategory = ({type, id=0}) => {
    this.setState({ selectedCategory: {type, id} }, this.fetchNextQuestion);
  }

  handleInputChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  }

  fetchNextQuestion = () => {
    const previousQuestions = [...this.state.pastQuestions];
    if (this.state.activeQuestion.id) {
      previousQuestions.push(this.state.activeQuestion.id);
    }

    $.ajax({
      url: '/quizzes',
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        previous_questions: previousQuestions,
        quiz_category: this.state.selectedCategory
      }),
      success: (data) => {
        this.setState({
          displayAnswer: false,
          pastQuestions: previousQuestions,
          activeQuestion: data.question,
          userAnswer: '',
          endGame: data.question ? false : true
        });
      },
      error: () => {
        alert('Unable to load a new question. Please try again.');
      }
    });
  }

  submitAnswer = (event) => {
    event.preventDefault();
    const cleanGuess = this.state.userAnswer.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase();
    const isCorrect = this.checkAnswer();
    this.setState({
      correctAnswersCount: isCorrect ? this.state.correctAnswersCount + 1 : this.state.correctAnswersCount,
      displayAnswer: true,
    });
  }

  checkAnswer = () => {
    const cleanGuess = this.state.userAnswer.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase();
    const correctAnswers = this.state.activeQuestion.answer.toLowerCase().split(' ');
    return correctAnswers.includes(cleanGuess);
  }

  resetGame = () => {
    this.setState({
      selectedCategory: null,
      pastQuestions: [],
      displayAnswer: false,
      correctAnswersCount: 0,
      activeQuestion: {},
      userAnswer: '',
      endGame: false
    });
  }

  renderCategorySelection() {
    return (
      <div className="quiz-start">
        <div className="select-header">Choose a Category</div>
        <div className="category-list">
          <div className="category-item" onClick={() => this.chooseCategory({ type: 'ALL' })}>ALL</div>
          {Object.keys(this.state.allCategories).map((id) => (
            <div
              key={id}
              className="category-item"
              onClick={() => this.chooseCategory({ type: this.state.allCategories[id], id })}
            >
              {this.state.allCategories[id]}
            </div>
          ))}
        </div>
      </div>
    );
  }

  renderFinalScore() {
    return (
      <div className="quiz-end">
        <div className="final-score">Your Final Score: {this.state.correctAnswersCount}</div>
        <div className="play-again-button" onClick={this.resetGame}>Play Again?</div>
      </div>
    );
  }

  renderAnswerFeedback() {
    const isCorrect = this.checkAnswer();
    return (
      <div className="quiz-feedback">
        <div className="question-display">{this.state.activeQuestion.question}</div>
        <div className={isCorrect ? 'correct' : 'incorrect'}>
          {isCorrect ? "Correct!" : "Incorrect"}
        </div>
        <div className="answer-display">Correct Answer: {this.state.activeQuestion.answer}</div>
        <div className="next-button" onClick={this.fetchNextQuestion}>Next Question</div>
      </div>
    );
  }

  renderGamePlay() {
    return this.state.pastQuestions.length === maxQuestionsPerGame || this.state.endGame
      ? this.renderFinalScore()
      : this.state.displayAnswer
        ? this.renderAnswerFeedback()
        : (
          <div className="quiz-play">
            <div className="question-display">{this.state.activeQuestion.question}</div>
            <form onSubmit={this.submitAnswer}>
              <input type="text" name="userAnswer" onChange={this.handleInputChange} />
              <input className="submit-button" type="submit" value="Submit Answer" />
            </form>
          </div>
        );
  }

  render() {
    return this.state.selectedCategory
      ? this.renderGamePlay()
      : this.renderCategorySelection();
  }
}

export default QuizGame;
