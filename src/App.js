import React, { useState, useEffect } from 'react';
import './App.css';
import 'bulma/css/bulma.css'

function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <div className="App">
      <p>URL Shortener</p>
      <div className="container">
        <div className="notification">
          <div className="field has-addons is-large">
            <div className="control">

              {/* bool: readOnly */}
              <input className="input is-large" type="text" placeholder={currentTime} readOnly={false} />
            </div>
            <div className="control">

              {/* bool(style): is-loading */}
              <a className="button is-info is-large">
                Search
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
