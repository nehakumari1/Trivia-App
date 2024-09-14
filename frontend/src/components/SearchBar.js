import React, { Component } from 'react';

class SearchBar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      searchTerm: '',
    };
  }

  handleSubmit = (event) => {
    event.preventDefault();
    this.props.onSearch(this.state.searchTerm);
  }

  handleChange = (event) => {
    this.setState({
      searchTerm: event.target.value
    });
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <input
          type="text"
          placeholder="Search for questions..."
          value={this.state.searchTerm}
          onChange={this.handleChange}
        />
        <button type="submit" className="search-button">Search</button>
      </form>
    );
  }
}

export default SearchBar;
