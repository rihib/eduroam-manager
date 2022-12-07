import requests
import json
import boto3
import config
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decimal import Decimal

def lambda_handler(event, context):
    access_token = event["rawQueryString"][11:]
    
    if access_token == "AuthN Error":
        result = access_token
    else:
        wide_user_email = get_wide_user_email(access_token)
        
        if wide_user_email[:53] == "Failed to connect to aws or access_token is expired. ": # TODO: ダサいので正規表現を使うか、そもそもこういうコードを書かなくて済むようにリファクタするか
            result = wide_user_email
        else:
            wide_number = get_wide_number(wide_user_email)
            result = wide_number
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }

# def get_access_token(authz_code):
#     # TODO: 最初にCookie等にaccess_tokenが保存されていないか調べて、保存されていたらそれを使うようにしたい。
#     try:
#         payload = {
#             'Content-Type': 'application/x-www-form-urlencoded', 
#             'grant_type': 'authorization_code', 
#             'client_id': config.CLIENT_ID, 
#             'code': authz_code, 
#             'redirect_uri': "http://localhost:3000/" # 'https://doc2xmjzxoyxn.cloudfront.net'
#         }
#         response = requests.post(config.COGNITO_URL, data=payload)
#         # TODO: トークンを取得したら、Cookie等に保存したい。
#         access_token = response.json()["access_token"]
#         return access_token
#     except Exception as err:
#         return f"Authorization Code is expired. Please logout and login again.: {err}"
    
def get_wide_user_email(access_token):
    try:
        aws_client = boto3.client(
            'cognito-idp', 
            region_name = config.REGION_NAME, 
            aws_access_key_id = config.AWS_ACCESS_KEY_ID, 
            aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY
        )
        result = aws_client.get_user(AccessToken = access_token)
        wide_user_email = result["UserAttributes"][2]["Value"]
        return wide_user_email
    except Exception as err:
        # TODO: access_tokenが有効期限切れ(1h)ならCookie等に保存してあるrefresh_tokenを使用して再度有効なaccess_tokenを取得するようにしたい。
        return f"Failed to connect to aws or access_token is expired. Please logout and login again.: {err}"
    
def get_wide_number(wide_user_email):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("wide_eduroam")
    
    try:
        response = table.query(
            IndexName='email-index',
            KeyConditionExpression=Key('email').eq(wide_user_email)
        )   
    except ClientError as err:
        err_code = err.response['Error']['Code']
        err_message = err.response['Error']['Message']
        return f"{err_code}: {err_message}"
    else:
        try:
            return int(response['Items'][0]["id"])
        except KeyError:
            return "Invalid response"