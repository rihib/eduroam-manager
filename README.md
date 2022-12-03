# eduroamゲストアカウント配布サイト
メンバーにeduroamゲストアカウントを配布するWebアプリ（[参照](https://github.com/wide-camp/widecamp2303/issues/2)）。

## オペレーションフローチャート

<img width="6147" alt="operation_flow_chart" src="https://user-images.githubusercontent.com/76939037/203570632-b1d5af92-fbce-4188-b94a-22ccc09a5ecf.png">

## デプロイ
1. 以下のコマンドを実行
    ```
    $ npm run build
    $ npm run devBuild
    ```
1. S3に`/build`以下のファイル・フォルダを置く