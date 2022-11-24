// import logo from './logo.svg';
// import './App.css';
import axios from 'axios';
import React from 'react';
import parse from 'html-react-parser';

const baseURL = 'https://5ggrco4pfi.execute-api.ap-northeast-1.amazonaws.com/1/dispatcher'

function App() {
  const [page, setPage] = React.useState(null);
  const [error, setError] = React.useState(null);

  React.useEffect(() => {
    axios
      .get(baseURL)
      .then((response) => {
        setPage(response.data);
      })
      .catch(error => {
        setError(error);
      });
  }, []);

  if (error) return `Oops, looks like an error.: ${error.message}`;

  const message = 'Oops, I cannot get the page data.'
  if (!page) return message;
  if (!page.body) return message;

  let html_textdata = page.body;
  html_textdata = html_textdata.slice(1);
  html_textdata = html_textdata.slice(0, -1);

  return (
    <div>
      {parse(html_textdata)}
    </div>
  );
}

export default App;