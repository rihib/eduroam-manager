import boto3
import json
import requests
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decimal import Decimal

EDUROAM_INFO_HTML_PATH = "eduroam_info.html"

def lambda_handler(event, context):
    wide_number = get_wide_number()
    if type(wide_number) is int:
        wide_user_info = get_wide_user_info(wide_number)
        
        try:
            wide_user_name = wide_user_info["name"]
            wide_user_email = wide_user_info["email"]
            result = get_eduroam_account_info_and_wide_user_info(wide_number, wide_user_name, wide_user_email)
        except Exception as err:
            result = wide_user_info
    else:
        result = wide_number
    
    return {
        'statusCode': 200,
        'body': json.dumps(str(result), default=decimal_default_proc, ensure_ascii=False)
    }

def get_wide_number():
    try:
        wide_number_response_obj = requests.get("https://jsonplaceholder.typicode.com/users/1") # TODO: プレースホルダーを実際のAPIにリプレースする
        wide_number_response_obj.raise_for_status()
        wide_number = wide_number_response_obj.json()["id"] # TODO: "id"を"wide_number"に直す
        return wide_number
    
    except requests.exceptions.RequestException as err:
        return err
    
    except Exception as err:
        return err

def get_wide_user_info(wide_number):
    try:
        payload = {"wide_number": wide_number}
        response_obj = requests.get("https://glaw74iufsxjctmj372zs5wo4q0yoaar.lambda-url.ap-northeast-1.on.aws/", params=payload)
        response_obj.raise_for_status()
        
        response = response_obj.json()
        
        if response == "WIDE number does not exist":
            raise Exception("WIDE number does not exist")
        
        eduroam_account_data = response["eduroam_account_info"]
        wide_user_data = response["wide_user_info"]
        
        if eduroam_account_data == "Invalid association":
            raise Exception("Invalid association")
        
        if eduroam_account_data == "unissued":
            return wide_user_data
        else:
            raise Exception("Issued")
    
    except requests.exceptions.RequestException as err:
        return err
    
    except Exception as err:
        return err
    
def get_eduroam_account_info_and_wide_user_info(wide_number, wide_user_name, wide_user_email):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("wide_eduroam")
    
    try:
        response = table.query(
            IndexName="flag-index",
            KeyConditionExpression=Key("type").eq("eduroam_account") & Key("flag").eq(1)
        )
    except ClientError as err:
        err_code = err.response['Error']['Code']
        err_message = err.response['Error']['Message']
        return f"{err_code}: {err_message}"
    else:
        try:
            eduroam_account_info = response['Items'][0] 
            # TODO: flagが1のアイテムが複数返ってくることがあるかもしれない。
            # その場合、おそらくその後のeduroam_account_info["info"]でエラーになると思うが一応例外処理を加えておきたい。
            # 複数返ってきた場合にどのようなフォーマットになるのかを確認する必要がある。
            
            if eduroam_account_info["associated_wide_user_id"] != Decimal(0):
                raise Exception("Invalid response")
            
            eduroam_account_data = eduroam_account_info["info"]
            eduroam_account_id = eduroam_account_info["id"]
            
            # id = eduroam_account_id のeduroamアカウントについて、associated_wide_user_id = wide_number, flag = 0 に更新する。
            try:
                table.update_item(
                    Key={'type': "eduroam_account", 'id': eduroam_account_id},
                    UpdateExpression="set associated_wide_user_id=:n, flag=:f",
                    ExpressionAttributeValues={
                        ':n': Decimal(wide_number), ':f': Decimal(0)},
                    ReturnValues="UPDATED_NEW")
            except ClientError as err:
                err_code = err.response['Error']['Code']
                err_message = err.response['Error']['Message']
                return f"{err_code}: {err_message}"
            except Exception as err:
                return err
            
            # id = eduroam_account_id + 1 のeduroamアカウントについて、flag = 1 に更新する。idが存在しない場合は、配り終わったことを返す
            try:
                table.update_item(
                    Key={'type': "eduroam_account", 'id': eduroam_account_id + Decimal(1)},
                    UpdateExpression="set flag=:f",
                    ExpressionAttributeValues={':f': Decimal(1)},
                    ReturnValues="UPDATED_NEW")
            except ClientError as err:
                err_code = err.response['Error']['Code']
                err_message = err.response['Error']['Message']
                return f"{err_code}: {err_message}"
            except Exception as err:
                return err
            
            # id = wide_number のwideユーザーにアクセスして、associated_eduroam_account_id = eduroam_account_id に更新する。
            try:
                table.update_item(
                    Key={'type': "wide_user", 'id': Decimal(wide_number)},
                    UpdateExpression="set associated_eduroam_account_id=:i",
                    ExpressionAttributeValues={':i': eduroam_account_id},
                    ReturnValues="UPDATED_NEW")
            except ClientError as err:
                err_code = err.response['Error']['Code']
                err_message = err.response['Error']['Message']
                return f"{err_code}: {err_message}"
            except Exception as err:
                return err
            
            # 返り値を作る
            with open(EDUROAM_INFO_HTML_PATH) as f:
                html_textdata = f.read()
            
            user_name_list = wide_user_name
            user_name = ""
            for name in user_name_list:
                user_name += name
                user_name += "　"
            user_name = user_name[:-1]
            
            html_textdata = html_textdata.format(
                eduroam_account_username = eduroam_account_data["username"],
                eduroam_account_password = eduroam_account_data["password"], 
                user_name = user_name
            )
            
            html_textdata = html_textdata.replace("\n", "")
            return html_textdata
            
        except KeyError:
            return "Invalid response"
        
        except Exception as err:
            return err

def decimal_default_proc(obj):
    """
    Convert object of type decimal to int.

    :param obj: An object that not JSON serializable.
    :return: An int object.
    """
    if type(obj) is Decimal:
        return int(obj)
    raise TypeError