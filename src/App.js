import './App.css';
import axios from 'axios';
import React from 'react';
import parse from 'html-react-parser';
import { TermAndConditions } from './TermAndConditions';
import { getAuthZCode } from './getAuthZCode';

function App() {
  const dispatcherAPIURL = 'https://5ggrco4pfi.execute-api.ap-northeast-1.amazonaws.com/1/dispatcher';
  const [page, setPage] = React.useState(null);
  const [error, setError] = React.useState(null);

  React.useEffect(() => {
    let accessToken = getAuthZCode(); // TODO: 実際はaccessTokenを取得しているので、名前を直すか、Cognito@Edgeを使わずに自分で実装して、認証コードを使うようにするか、どっちかにする
    const options = {
      params: {
        AuthZCode: accessToken // TODO: 実際はaccessTokenを取得しているので、名前を直すか、Cognito@Edgeを使わずに自分で実装して、認証コードを使うようにするか、どっちかにする
      }
    }

    axios
      .get(dispatcherAPIURL, options)
      .then(response => {
        setPage(response.data);
      })
      .catch(error => {
        setError(error);
      });
  }, []);

  // TODO: `Oops, looks like an error.'や、'Please wait.'、apiから返されるHTMLを使う代わりに
  // React上で、JSXでHTMLを作って、それを返すように変更する。
  // なので、apiはHTMLではなく、HTMLファイルの名前と引数をJSONで返すようにする。
  // それらのJSXで作るHTMLは別のファイルからインポートする形にすることで他の箇所でも再利用できるようにする。

  if (error) return `Oops, looks like an error.: ${error.message}`;

  const message = 'Please wait.'
  if (!page) return message;
  if (!page.body) return message;

  let html_textdata = page.body;
  html_textdata = html_textdata.slice(1);
  html_textdata = html_textdata.slice(0, -1);
  html_textdata = html_textdata.replace(/\\/g, "");

  // TODO: apiから返されたHTMLファイルの名前で条件分岐するように変更する。
  if (html_textdata.substr(4, 17) === "Term & Conditions") {
    return (
      <div>
        {parse(html_textdata)}
        <TermAndConditions />  {/* TODO: apiから返された引数を渡す */}
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