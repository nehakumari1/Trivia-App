import React, { Component } from 'react'; 
import $ from 'jquery';
import '../stylesheets/FormView.css';

class FormView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
      categories: {}
    };
  }

  // Fetch categories once the component is mounted
  componentDidMount() {
    $.ajax({
      url: '/categories',  // Make a GET request to fetch available categories
      type: 'GET',
      success: (response) => {
        this.setState({ categories: response.categories });
      },
      error: (err) => {
        alert('Error loading categories. Please try again.');
      }
    });
  }

  // Handle form submission to add a new question
  submitQuestion = (event) => {
    event.preventDefault();
    
    const { question, answer, difficulty, category } = this.state;

    $.ajax({
      url: '/questions',  // Make a POST request to add a new question
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: question,
        answer: answer,
        difficulty: difficulty,
        category: category
      }),
      success: (result) => {
        // Reset form after successful submission
        document.getElementById('add-question-form').reset();
      },
      error: (err) => {
        alert('Error submitting the question. Please try again.');
      }
    });
  }

  // Update state when form fields change
  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  }

  // Render the form to create a new trivia question
  render() {
    return (
      <div id="add-form">
        <h2>Create a New Trivia Question</h2>
        <form id="add-question-form" className="form-view" onSubmit={this.submitQuestion}>
          <label>
            Question:
            <input type="text" name="question" onChange={this.handleChange} />
          </label>
          <label>
            Answer:
            <input type="text" name="answer" onChange={this.handleChange} />
          </label>
          <label>
            Difficulty:
            <select name="difficulty" onChange={this.handleChange}>
              <option value="1">1 (Easy)</option>
              <option value="2">2</option>
              <option value="3">3 (Medium)</option>
              <option value="4">4</option>
              <option value="5">5 (Hard)</option>
            </select>
          </label>
          <label>
            Category:
            <select name="category" onChange={this.handleChange}>
              {Object.entries(this.state.categories).map(([id, name]) => (
                <option key={id} value={id}>{name}</option>
              ))}
            </select>
          </label>
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default FormView;
