export function getAuthZCode() { // TODO: 実際はaccessTokenを取得しているので、名前を直すか、Cognito@Edgeを使わずに自分で実装して、認証コードを使うようにするか、どっちかにする
    let cookieArray = document.cookie.split(';');
    let accessToken = "";
    
    if (cookieArray) {
        cookieArray.forEach(
            function (value) {
                if (value.indexOf("accessToken") !== -1) {
                    accessToken = value.split('=')[1];
                }
            }
        );
    }

    if (accessToken) {
        accessToken = accessToken.replace(/"/g, '');
        return accessToken;
    } else {
        return "AuthN Error";
    }
}