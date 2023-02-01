# eduroamゲストアカウント配布サイト
メンバーにeduroamゲストアカウントを配布するWebアプリ（[参照](https://github.com/wide-camp/widecamp2303/issues/2)）。\
\
初回使用時のシステムの詳細については[この記事](https://rihib.dev/ac7ac9df-9564-46e7-beed-fe603c436b22.html)を参照。\

## オペレーションフローチャート

<img width="6147" alt="operation_flow_chart" src="https://user-images.githubusercontent.com/76939037/203570632-b1d5af92-fbce-4188-b94a-22ccc09a5ecf.png">

## デプロイ
1. 以下のコマンドを実行
    ```
    $ npm run build
    $ npm run devBuild
    ```
1. S3に`/build`以下のファイル・フォルダを置く