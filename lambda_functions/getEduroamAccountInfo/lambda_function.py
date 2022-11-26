import boto3
import json
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decimal import Decimal

def lambda_handler(event, context):
    wide_number = int(event["queryStringParameters"]["wide_number"])
    wide_user_info = get_info("wide_user", wide_number)
    
    if wide_user_info == "Invalid response":
        result == "WIDE number does not exist"
    else:
        associated_eduroam_account_id = wide_user_info["associated_eduroam_account_id"]
        wide_user_info = wide_user_info["info"]
        
        if associated_eduroam_account_id == 0:
            eduroam_account_info = "unissued"
        else:
            eduroam_account_info = get_info("eduroam_account", associated_eduroam_account_id)
            
            if eduroam_account_info["associated_wide_user_id"] != associated_eduroam_account_id:
                eduroam_account_info == "Invalid association"
            else:
                eduroam_account_info = eduroam_account_info["info"]
        result = {"wide_user_info": wide_user_info, "eduroam_account_info": eduroam_account_info}
    
    return {
        'statusCode': 200,
        'body': json.dumps(result, default=decimal_default_proc, ensure_ascii=False)
    }

def get_info(type, id):
    """
    Gets info of the wide user or the eduroam account.

    :param type: The type which "wide_user" or "eduroam_account".
    :param id: The id of the wide user or the eduroam account.
    :return: The info of the wide user or the eduroam account.
    """
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("eduroam_account_distributor")
    
    try:
        response = table.get_item(Key={"type": type, 'id': id})
    except ClientError as err:
        err_code = err.response['Error']['Code']
        err_message = err.response['Error']['Message']
        return f"{err_code}: {err_message}"
    else:
        try:
            return response['Item']
        except KeyError:
            return "Invalid response"

def decimal_default_proc(obj):
    """
    Convert object of type decimal to int.

    :param obj: An object that not JSON serializable.
    :return: An int object.
    """
    if type(obj) is Decimal:
        return int(obj)
    raise TypeError