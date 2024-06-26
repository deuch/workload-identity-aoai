import os
import httpx
import json
from openai import AzureOpenAI
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

client = AzureOpenAI(
      api_version=OPENAI_API_VERSION,
      azure_endpoint=AZURE_OPENAI_ENDPOINT,
      api_key="FAKE_KEY",
      http_client=httpx.Client(auth=auth)
  )


# Loop to check if the token is retrieved from cache

for i in range(1, 4):

  completion = client.chat.completions.create(
      model=AZURE_OPENAI_DEPLOYMENT_NAME,  # e.g. gpt-35-instant
      messages=[
          {
              "role": "user",
              "content": "How do I output all files in a directory using Python?",
          },
      ]
  )
  print(completion.choices[0].message.content)

