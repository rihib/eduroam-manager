import os
from dotenv import load_dotenv

load_dotenv()

COGNITO_URL = os.getenv("COGNITO_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
REGION_NAME = os.getenv("REGION_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
USER_POOL_ID = os.getenv("USER_POOL_ID")
CLIENT_ID = os.getenv("CLIENT_ID")