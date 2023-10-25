import json
import requests

def get_token():

    #Define
    tenant_id= 'sample_tetant_id'
    client_id = 'sample_client_id'
    client_secret = 'sample_client_secret'
    #Grab token
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host':'login.microsoftonline.com:443'
    }

    data = {
        'grant_type': 'client_credentials',
        'scope': 'https://analysis.windows.net/powerbi/api/.default',
        'client_id': client_id,
        'client_secret': client_secret
    }

    result = requests.post('https://login.microsoftonline.com/{0}/oauth2/v2.0/token'.format(tenant_id), headers= header, data = data)

    #Get latest Power BI Dataset Refresh
    access_token = result.json()['access_token']

    return access_token