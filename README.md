# Workload Identity for Azure OpenAI and Auth0

This repo will help you to use a Workload Identity to connect to Azure OpenAI with an identity in [Auth0](https://auth0.com/).

An API/identity (clientID/clientSecret) is created in an Auth0 domain. This identity is used to authenticate to Auth0 and retrieve an acces_token.  

This token is used to authenticate to Azure Entra ID with a binding on a User Managed Identity (Federated Credentials).

Please find some [documentation](https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation#how-it-works) about the concept of workload identity.

Use the client credential flow as explained [here](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-client-creds-grant-flow#third-case-access-token-request-with-a-federated-credential)

## Auth0

You can signup to a free account on [Auth0](https://auth0.com/)

1. Create an API :

![API in Auth0](./img/1.png)

2. Use **api://AzureADTokenExchange** in the Audience

![API in Auth0](./img/2.png)

3. Retrieve and keep those informations :
  - Domain
  - Client ID
  - Client Secret

![API in Auth0](./img/3.png)

## Managed Identity

1. Create a User Managed Identity and add a Federated credential

![API in Auth0](./img/4.png)

2. Configure the Federated Credentials

- Issuer URL : https:// + Auth0 Domain  
- Subject Identifier : Auth0 Client ID + **@clients**  
- Name : The name you want
- Keep the same audience as set in Auth0 : **api://AzureADTokenExchange**

![API in Auth0](./img/5.png)

## Pre-requisites

- One Azure OpenAI instance with a model deployed
- The User Managed Identity must have the role *Cognitive Services OpenAI User*

## Python

- You need to install all the package in the requirements file
  - `pip install requirements.txt`
- Rename the **.env-sample** file to **.env**
- Fill all the values
- Run the code
  - `python aoai.py`

## Deployment parameters

| Parameter | Value | Note |
| --- | --- | ------------- |
|OIDC_ENDPOINT||Auth0 domain (without https)|
|OIDC_CLIENT_ID||Auth0 clientID| 
|OIDC_CLIENT_SECRET||Auth0 client Secret|
|AZURE_TENANT_ID||ID of your Entra ID tenant|
|AZURE_CLIENT_ID||ClientID of the User Managed Identity|
|AZURE_AOAI_ENDPOINT||Endpoint of the Azure OpenAI resource (with https)|
|AZURE_AOAI_MODEL_DEPLOYMENT_NAME||Deployment name of your gpt model|
|AZURE_AOAI_API_VERSION|2023-07-01-preview|API version of Azure OpenAI|


