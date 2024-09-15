import React from 'react';
import ReactDOM from 'react-dom';
import './stylesheets/index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';

// Render the main App component into the root DOM element
ReactDOM.render(<App />, document.getElementById('root'));

// For offline functionality and faster load times, switch
// `unregister()` to `register()`. Be aware that it may introduce
// certain challenges. Learn more about service workers here: https://bit.ly/CRA-PWA
serviceWorker.unregister();
