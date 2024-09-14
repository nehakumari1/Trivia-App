import React, { Component } from 'react'; 
import logo from '../logo.svg';
import '../stylesheets/Header.css';

class Header extends Component {

  // Navigate to the specified path
  redirectTo(path) {
    const baseUrl = window.location.origin;
    window.location.href = baseUrl + path;
  }

  render() {
    return (
      <header className="App-header">
        <h1 onClick={() => this.redirectTo('/')}>Trivia Master</h1>
        <h2 onClick={() => this.redirectTo('/')}>Questions List</h2>
        <h2 onClick={() => this.redirectTo('/add')}>Add Question</h2>
        <h2 onClick={() => this.redirectTo('/play')}>Start Game</h2>
      </header>
    );
  }
}

export default Header;
