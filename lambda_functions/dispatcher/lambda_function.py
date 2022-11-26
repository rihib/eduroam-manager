import json
import requests

TERMS_AND_CONDITIONS_HTML_PATH = "term_and_conditions.html"
EDUROAM_INFO_HTML_PATH = "eduroam_info.html"
ERR_HTML_PATH = "error.html"

# TODO: API Gatewayの'Access-Control-Allow-Origin'をS3のものに変更
def lambda_handler(event, context):
    html_path_and_arguments = get_html_path_and_arguments()
    html_textdata = get_html_textdata(html_path_and_arguments)
    
    return {
        'statusCode': 200,
        'body': json.dumps(html_textdata)
    }

def get_html_path_and_arguments():
    html_path_and_arguments = {}
    
    try:
        wide_number_response_obj = requests.get("https://jsonplaceholder.typicode.com/users/1") # TODO: プレースホルダーを実際のAPIにリプレースする
        wide_number_response_obj.raise_for_status()
        wide_number = wide_number_response_obj.json()["id"] # TODO: "id"を"wide_number"に直す
        
        if type(wide_number) is int:
            try:
                payload = {"id": wide_number} # TODO: "id"を"wide_number"に直す
                eduroam_account_data_response_obj = requests.get("https://glaw74iufsxjctmj372zs5wo4q0yoaar.lambda-url.ap-northeast-1.on.aws/", params=payload)
                eduroam_account_data_response_obj.raise_for_status()
                eduroam_account_data = eduroam_account_data_response_obj.json()[0]["address"]["geo"] # TODO: APIにあった形に直す
                user_name = eduroam_account_data_response_obj.json()[0]["name"] # TODO: APIにあった形に直す
                user_email = eduroam_account_data_response_obj.json()[0]["email"] # TODO: APIにあった形に直す
                
                if eduroam_account_data == "unissued":
                    html_path_and_arguments["html_path"] = TERMS_AND_CONDITIONS_HTML_PATH
                    html_path_and_arguments["user_name"] = user_name
                elif eduroam_account_data == "WIDE number does not exist":
                    raise Exception("WIDE number does not exist")
                else:
                    try:
                        html_path_and_arguments["html_path"] = EDUROAM_INFO_HTML_PATH
                        html_path_and_arguments["eduroam_account_username"] = eduroam_account_data["lat"] # TODO: "lat"を"username"に直す
                        html_path_and_arguments["eduroam_account_password"] = eduroam_account_data["lng"] # TODO: "lng"を"password"に直す
                        html_path_and_arguments["user_name"] = user_name
                    except:
                        html_path_and_arguments["html_path"] = ERR_HTML_PATH
                        html_path_and_arguments["error_message"] = "Invalid eduroam account data"
            
            except requests.exceptions.RequestException as err:
                html_path_and_arguments["html_path"] = ERR_HTML_PATH
                html_path_and_arguments["error_message"] = err
            
            except Exception as err:
                html_path_and_arguments["html_path"] = ERR_HTML_PATH
                html_path_and_arguments["error_message"] = err
    
        else:
            raise Exception("Cannot get WIDE number")
        
    except requests.exceptions.RequestException as err:
        html_path_and_arguments["html_path"] = ERR_HTML_PATH
        html_path_and_arguments["error_message"] = err
    
    except Exception as err:
        html_path_and_arguments["html_path"] = ERR_HTML_PATH
        html_path_and_arguments["error_message"] = err
    
    return html_path_and_arguments

def get_html_textdata(html_path_and_arguments):
    html_path = html_path_and_arguments["html_path"]
    
    with open(html_path) as f:
        html_textdata = f.read()
        
    if html_path == TERMS_AND_CONDITIONS_HTML_PATH:
        html_textdata = html_textdata.format(
            user_name = html_path_and_arguments["user_name"]
            )
    
    if html_path == EDUROAM_INFO_HTML_PATH:
        html_textdata = html_textdata.format(
            eduroam_account_username = html_path_and_arguments["eduroam_account_username"], 
            eduroam_account_password = html_path_and_arguments["eduroam_account_password"],
            user_name = html_path_and_arguments["user_name"]
            )
    
    if html_path == ERR_HTML_PATH:
        html_textdata = html_textdata.format(
            error_message = html_path_and_arguments["error_message"]
            )
            
    html_textdata = html_textdata.replace("\n", "")
    
    return html_textdata