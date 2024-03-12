import os
import json
import http.client
from openai import AzureOpenAI
from dotenv import load_dotenv
from azure.identity import ClientAssertionCredential, get_bearer_token_provider

#To retrieve the token of the OIDC provider
def get_assertion():

  conn = http.client.HTTPSConnection(OIDC_ENDPOINT)

  data = {}
  data['client_id'] = OIDC_CLIENT_ID
  data['client_secret'] = OIDC_CLIENT_SECRET
  data['audience'] = "api://AzureADTokenExchange"
  data['grant_type'] = "client_credentials" 
  
  payload = json.dumps(data)
  
  headers = { 'content-type': "application/json" }
  # Call Auth0 OIDC provider
  conn.request("POST", "/oauth/token", payload, headers)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))
  result = json.loads(data.decode('utf-8'))
  return result['access_token']
  
load_dotenv()

OIDC_ENDPOINT=os.environ.get('OIDC_ENDPOINT')
OIDC_CLIENT_ID=os.environ.get('OIDC_CLIENT_ID')
OIDC_CLIENT_SECRET=os.environ.get('OIDC_CLIENT_SECRET')
AZURE_TENANT_ID=os.environ.get('AZURE_TENANT_ID')
AZURE_CLIENT_ID=os.environ.get('AZURE_CLIENT_ID')
AZURE_AOAI_ENDPOINT=os.environ.get('AZURE_AOAI_ENDPOINT')
AZURE_AOAI_MODEL_DEPLOYMENT_NAME=os.environ.get('AZURE_AOAI_MODEL_DEPLOYMENT_NAME')
AZURE_AOAI_API_VERSION=os.environ.get('AZURE_AOAI_API_VERSION')

credential = ClientAssertionCredential(
       tenant_id=AZURE_TENANT_ID,
       client_id=AZURE_CLIENT_ID,
       func=get_assertion,
)

# Use the Workload Identity ro retrieve a token for Azure OpenAI
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

# may change in the future
# https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
api_version = AZURE_AOAI_API_VERSION

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=AZURE_AOAI_ENDPOINT,
    azure_ad_token_provider=token_provider,
)

completion = client.chat.completions.create(
    model=AZURE_AOAI_MODEL_DEPLOYMENT_NAME,  # e.g. gpt-35-instant
    messages=[
        {
            "role": "user",
            "content": "How do I output all files in a directory using Python?",
        },
    ],
)

print(completion.choices[0].message.content)
