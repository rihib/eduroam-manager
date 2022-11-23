// import logo from './logo.svg';
// import './App.css';
import axios from 'axios';
import React from 'react';
import parse from 'html-react-parser';

const baseURL = 'https://mockend.com/rihib/Mockend/pages/1'

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

  if (error) return `おっと、エラーみたいですね： ${error.message}`;

  const message = 'おっと、どうやらページデータを取得できなかったようです。'
  if (!page) return message;
  if (!page.data) return message;

  return (
    <div>
      {parse(page.data)}
    </div>
  );
}

export default App;