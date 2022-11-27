import axios from 'axios';
import React from 'react';
import parse from 'html-react-parser';
import { root } from './index.js'

export function TermAndConditions() {
  return (
    // TODO: JSXで渡された引数を埋め込む
    <div>
      <h1>Term & Conditions</h1>
      <h2>田中　太郎-san</h2>
      <p>This is Term & Conditions.</p>
      <button onClick={ DistributeEduroamAccounts }>
        Agree & Get Eduroam Account
      </button>
    </div>
  );
}

function DistributeEduroamAccounts() {
  const distributeAPIURL = 'https://5ggrco4pfi.execute-api.ap-northeast-1.amazonaws.com/1/distribute';
  // TODO: html_textdataではなく、作成したJSXファイルをインポートする形にする。
  let html_textdata = "";

  axios
    .put(distributeAPIURL)
    .then(response => {
      const page = response.data;
      if (page) {
        if (page.body) {
          html_textdata = page.body;
          html_textdata = html_textdata.slice(1);
          html_textdata = html_textdata.slice(0, -1);
        } else {
          html_textdata = 'Please wait.';
        }
      } else {
        html_textdata = 'Please wait.';
      }
    })
    .catch(error => {
      html_textdata = `Oops, looks like an err.: ${error.message}`;
    })
    .finally(() => {
      root.render(
        <React.StrictMode>
          <div>
            {parse(html_textdata)}
          </div>
        </React.StrictMode>
      );
    });
}