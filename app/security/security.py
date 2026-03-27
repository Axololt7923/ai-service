from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader
import os
import secrets
import dotenv

dotenv.load_dotenv()
# default incase of no env variable
FIXED_API_KEY = os.getenv("FIXED_API_KEY","random-api-key-12345678910")

# default true incase of no env variable
ENABLE_API_KEY = os.getenv("ENABLE_API_KEY", "True").lower() in "true"

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

def get_authorize(api_key: str = Security(api_key_header)):
    if ENABLE_API_KEY == "False":
        print("=======================================================================")
        print("API key is disabled")
        print("If you want to use API key, please set ENABLE_API_KEY=True in .env file")
        print("and make sure you have set FIXED_API_KEY in .env file")
        print("Default FIXED_API_KEY is: random-api-key-12345678910")
        print("=======================================================================")
        return api_key

    if not api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key is missing")

    if not secrets.compare_digest(api_key, FIXED_API_KEY):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")

    return api_key