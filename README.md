# eduroamゲストアカウント配布サイト
メンバーにeduroamゲストアカウントを配布するWebアプリ（[参照](https://github.com/wide-camp/widecamp2303/issues/2)）。\
\
初回使用時のシステムの詳細については[この記事](https://rihib.dev/ac7ac9df-9564-46e7-beed-fe603c436b22.html)を参照。\

## システムフロー図
<img width="6147" alt="システムフロー図" src="https://user-images.githubusercontent.com/76939037/216056001-ef9ada7a-f393-4317-9c75-7a489426d923.png">

## システムアーキテクチャ図
![10bd210f-dea6-4151-95f5-eb2fa25afc2a](https://user-images.githubusercontent.com/76939037/216056299-5ead09db-230f-447c-bb97-25be6d51c3a8.png)
<img width="6147" alt="システムアーキテクチャ図" src="https://user-images.githubusercontent.com/76939037/216056299-5ead09db-230f-447c-bb97-25be6d51c3a8.png">

## デプロイ
1. 以下のコマンドを実行
    ```
    $ npm run buil
    $ npm run devBuild
    ```
1. S3に`/build`以下のファイル・フォルダを置く
