// import logo from './logo.svg';
// import './App.css';
import axios from 'axios';
import React from 'react';
import parse from 'html-react-parser';
import { TermAndConditions } from './TermAndConditions';

function App() {
  const dispatcherAPIURL = 'https://5ggrco4pfi.execute-api.ap-northeast-1.amazonaws.com/1/dispatcher';
  const [page, setPage] = React.useState(null);
  const [error, setError] = React.useState(null);

  React.useEffect(() => {
    axios
      .get(dispatcherAPIURL)
      .then(response => {
        setPage(response.data);
      })
      .catch(error => {
        setError(error);
      });
  }, []);

  if (error) return `Oops, looks like an error.: ${error.message}`;

  const message = 'Please wait.'
  if (!page) return message;
  if (!page.body) return message;

  let html_textdata = page.body;
  html_textdata = html_textdata.slice(1);
  html_textdata = html_textdata.slice(0, -1);

  if (html_textdata === "<h1>Term & Conditions</h1><h2>田中　太郎-san</h2><p>This is Term & Conditions.</p>") {
    return (
      <div>
        <TermAndConditions />
      </div>
    );
  } else {
    return (
      <div>
        {parse(html_textdata)}
      </div>
    );
  }
}

export default App;