import os
import httpx
import json
from langchain_openai import AzureOpenAI
from dotenv import load_dotenv
from httpx_auth import OAuth2ClientCredentials

load_dotenv()

OIDC_ENDPOINT=os.environ.get('OIDC_ENDPOINT')
OIDC_CLIENT_ID=os.environ.get('OIDC_CLIENT_ID')
OIDC_CLIENT_SECRET=os.environ.get('OIDC_CLIENT_SECRET')
OIDC_SCOPE=os.environ.get('OIDC_SCOPE')
AZURE_OPENAI_ENDPOINT=os.environ.get('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_DEPLOYMENT_NAME=os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME')
AZURE_OPENAI_MODEL_NAME=os.environ.get('AZURE_OPENAI_MODEL_NAME')
OPENAI_API_VERSION=os.environ.get('OPENAI_API_VERSION')


# verify=False for debug purpose with proxy
# Will use an handler to store token in memory and refresh
oauth2_httpxclient=httpx.Client()
auth=OAuth2ClientCredentials(OIDC_ENDPOINT, client_id=OIDC_CLIENT_ID, client_secret=OIDC_CLIENT_SECRET, scope=OIDC_SCOPE, client=oauth2_httpxclient)

# Loop to check if the token is retrieved from cache

llm=AzureOpenAI(deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,model_name=AZURE_OPENAI_MODEL_NAME,http_client=httpx.Client(auth=auth))
question="How do I output all files in a directory using Python?"

print(llm.invoke(question))
print(llm)

