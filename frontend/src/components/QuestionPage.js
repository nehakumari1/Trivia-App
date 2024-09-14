import React, { Component } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionPage extends Component {
  constructor(){
    super();
    this.state = {
      questionList: [],
      currentPage: 1,
      totalQuestionsCount: 0,
      categoryList: {},
      activeCategory: null,
    };
  }

  componentDidMount() {
    this.fetchQuestions();
  }

  fetchQuestions = () => {
    $.ajax({
      url: `/questions?page=${this.state.currentPage}`, // Updated request URL
      type: "GET",
      success: (data) => {
        this.setState({
          questionList: data.questions,
          totalQuestionsCount: data.total_questions,
          categoryList: data.categories,
          activeCategory: data.current_category
        });
      },
      error: () => {
        alert('Failed to retrieve questions. Please try again.');
      }
    });
  }

  handlePageSelect = (pageNumber) => {
    this.setState({ currentPage: pageNumber }, this.fetchQuestions);
  }

  renderPagination(){
    const pages = [];
    const totalPages = Math.ceil(this.state.totalQuestionsCount / 10);
    
    for (let i = 1; i <= totalPages; i++) {
      pages.push(
        <span
          key={i}
          className={`page-number ${i === this.state.currentPage ? 'active' : ''}`}
          onClick={() => this.handlePageSelect(i)}
        >
          {i}
        </span>
      );
    }
    
    return pages;
  }

  fetchQuestionsByCategory = (categoryId) => {
    $.ajax({
      url: `/categories/${categoryId}/questions`, // Updated request URL
      type: "GET",
      success: (data) => {
        this.setState({
          questionList: data.questions,
          totalQuestionsCount: data.total_questions,
          activeCategory: data.current_category
        });
      },
      error: () => {
        alert('Failed to retrieve questions by category. Please try again.');
      }
    });
  }

  handleSearchSubmit = (searchQuery) => {
    $.ajax({
      url: `/search`, 
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ searchTerm: searchQuery }),
      success: (data) => {
        this.setState({
          questionList: data.questions,
          totalQuestionsCount: data.total_questions,
          activeCategory: data.current_category
        });
      },
      error: () => {
        alert('Search failed. Please try again.');
      }
    });
  }

  handleQuestionAction = (questionId) => (actionType) => {
    if (actionType === 'DELETE' && window.confirm('Are you sure you want to delete this question?')) {
      $.ajax({
        url: `/questions/${questionId}`,
        type: "DELETE",
        success: () => {
          this.fetchQuestions();
        },
        error: () => {
          alert('Failed to delete the question. Please try again.');
        }
      });
    }
  }

  render() {
    return (
      <div className="question-page">
        <div className="category-section">
          <h2 onClick={this.fetchQuestions}>Categories</h2>
          <ul>
            {Object.keys(this.state.categoryList).map((id) => (
              <li key={id} onClick={() => this.fetchQuestionsByCategory(id)}>
                {this.state.categoryList[id]}
                <img className="category-icon" src={`${this.state.categoryList[id]}.svg`} alt="category"/>
              </li>
            ))}
          </ul>
          <Search onSubmit={this.handleSearchSubmit} />
        </div>
        <div className="question-section">
          <h2>Questions</h2>
          {this.state.questionList.map((question) => (
            <Question
              key={question.id}
              question={question.question}
              answer={question.answer}
              category={this.state.categoryList[question.category]}
              difficulty={question.difficulty}
              questionAction={this.handleQuestionAction(question.id)}
            />
          ))}
          <div className="pagination-section">
            {this.renderPagination()}
          </div>
        </div>
      </div>
    );
  }
}

export default QuestionPage;
