import json
import requests

TERMS_AND_CONDITIONS_HTML_PATH = "term_and_conditions.html"
EDUROAM_INFO_HTML_PATH = "eduroam_info.html"
ERR_HTML_PATH = "err.html"

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
                payload = {"wide_number": wide_number}
                response_obj = requests.get("https://glaw74iufsxjctmj372zs5wo4q0yoaar.lambda-url.ap-northeast-1.on.aws/", params=payload)
                response_obj.raise_for_status()
                
                response = response_obj.json()
                
                if response == "WIDE number does not exist":
                    raise Exception("WIDE number does not exist")
                
                eduroam_account_data = response["eduroam_account_info"]
                wide_user_data = response_obj.json()["wide_user_info"]
                user_name_list = wide_user_data["name"]
                user_email = wide_user_data["email"]
                
                user_name = ""
                for name in user_name_list:
                    user_name += name
                    user_name += "　"
                user_name = user_name[:-1]
                
                if eduroam_account_data == "Invalid association":
                    raise Exception("Invalid association")
                
                if eduroam_account_data == "unissued":
                    html_path_and_arguments["html_path"] = TERMS_AND_CONDITIONS_HTML_PATH
                    html_path_and_arguments["user_name"] = user_name
                else:
                    try:
                        html_path_and_arguments["html_path"] = EDUROAM_INFO_HTML_PATH
                        html_path_and_arguments["eduroam_account_username"] = eduroam_account_data["username"]
                        html_path_and_arguments["eduroam_account_password"] = eduroam_account_data["password"]
                        html_path_and_arguments["user_name"] = user_name
                    except:
                        html_path_and_arguments["html_path"] = ERR_HTML_PATH
                        html_path_and_arguments["err_message"] = "Invalid eduroam account data"
            
            except requests.exceptions.RequestException as err:
                html_path_and_arguments["html_path"] = ERR_HTML_PATH
                html_path_and_arguments["err_message"] = err
            
            except Exception as err:
                html_path_and_arguments["html_path"] = ERR_HTML_PATH
                html_path_and_arguments["err_message"] = err
    
        else:
            raise Exception("Cannot get WIDE number")
        
    except requests.exceptions.RequestException as err:
        html_path_and_arguments["html_path"] = ERR_HTML_PATH
        html_path_and_arguments["err_message"] = err
    
    except Exception as err:
        html_path_and_arguments["html_path"] = ERR_HTML_PATH
        html_path_and_arguments["err_message"] = err
    
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
            err_message = html_path_and_arguments["err_message"]
            )
            
    html_textdata = html_textdata.replace("\n", "")
    
    return html_textdata