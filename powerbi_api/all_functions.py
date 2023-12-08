import json
import requests
import environ
import pandas as pd

env = environ.Env()
environ.Env.read_env()

def get_token():

    #Define
    tenant_id= env('pbi_tenant_id')
    client_id = env('pbi_app_id')
    client_secret = env('pbi_app_secret')
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

    result = requests.post(f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token', headers= header, data = data)

    #Get latest Power BI Dataset Refresh
    access_token = result.json()['access_token']

    return access_token

def get_header():
    # Get token
    access_token = get_token()
    # Define header
    header =     header = {
    'Content-Type':'application/json', 
    'Authorization':f'Bearer {access_token}'
    }

    return header

def get_all_workspaces(header):
    # Send API Request
    result = requests.get(url='https://api.powerbi.com/v1.0/myorg/groups', headers=header)
    # Convert to dataframe
    df_get_all_workspaces = pd.DataFrame.from_dict(result.json()['value'], orient ='columns')
    return df_get_all_workspaces

def get_all_datasets(header):

    # Set workspace list
    df_get_all_workspaces = get_all_workspaces(header)
    workspace_id_list = df_get_all_workspaces['id']
    # Define an empty dataframe
    df_get_all_datasets = pd.DataFrame()
    # Loop through workspace
    for workspace_id in workspace_id_list:
        workspace_name = df_get_all_workspaces.query('id == "{0}"'.format(workspace_id))["name"].iloc[0]
        # Define URL endpoint
        get_all_datasets_url =  'https://api.powerbi.com/v1.0/myorg/groups/{0}/datasets'.format(workspace_id)
        # Send API call to get data
        result = requests.get(url=get_all_datasets_url, headers=header)
        # If result success then proceed:
        if result.status_code == 200:
            # Create dataframe to store data
            df = pd.DataFrame.from_dict(result.json()['value'], orient ='columns')
            # Add workspace id column
            df['workspaceId'] = workspace_id
            # Add workspace name column
            df['workspaceName'] = workspace_name
            # Append data
            df_get_all_datasets = pd.concat([df_get_all_datasets,df])
    
    return df_get_all_datasets

def get_all_dataflows(header):

    # Set workspace list
    df_get_all_workspaces = get_all_workspaces(header)
    workspace_id_list = df_get_all_workspaces['id']
    # Define an empty dataframe
    df_get_all_dataflows = pd.DataFrame()
    # Loop through workspace
    for workspace_id in workspace_id_list:
        workspace_name = df_get_all_workspaces.query('id == "{0}"'.format(workspace_id))["name"].iloc[0]
        # Define URL endpoint
        get_all_dataflows_url =  f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/dataflows'
        # Send API call to get data
        result = requests.get(url=get_all_dataflows_url, headers=header)
        # If result success then proceed:
        if result.status_code == 200:
            # Create dataframe to store data
            df = pd.DataFrame.from_dict(result.json()['value'], orient ='columns')
            # Add column
            df['workspaceId'] = workspace_id
            # Add workspace name column
            df['workspaceName'] = workspace_name
            # Append data
            df_get_all_dataflows = pd.concat([df_get_all_dataflows,df])
    return df_get_all_dataflows

def get_all_reports(header):

    # Set workspace list
    df_get_all_workspaces = get_all_workspaces(header)
    # Set workspace list
    workspace_id_list = df_get_all_workspaces['id']
    # Define an empty dataframe
    df_get_all_reports = pd.DataFrame()
    # Loop through workspace
    for workspace_id in workspace_id_list:
        workspace_name = df_get_all_workspaces.query('id == "{0}"'.format(workspace_id))["name"].iloc[0]
        # Define URL endpoint
        get_all_reports_url =  f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports'
        # Send API call to get data
        result = requests.get(url=get_all_reports_url, headers=header)
        # If result success then proceed:
        if result.status_code == 200:
            # Create dataframe to store data
            df = pd.DataFrame.from_dict(result.json()['value'], orient ='columns')
            # Add workspace name column
            df['workspaceName'] = workspace_name
            # Append data
            df_get_all_reports = pd.concat([df_get_all_reports,df])
    return df_get_all_reports


def refresh_dataflow(header, workspace_id,dataflow_id):
    # Define URL
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/dataflows/{dataflow_id}/refreshes'
    # Send POST request
    result = requests.post(url, headers= header)
    # Print message
    print(f'Start refreshing dataflow {dataflow_id}')
    
def refresh_dataset(header, workspace_id,dataset_id):
    # Define URL
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/refreshes'
    # Send POST request
    result = requests.post(url, headers= header)
    # Print message
    print(f'Start refreshing dataset {dataset_id}')
    
def get_all_report_users(header,workspace_id,report_id):

    # Set workspace list
    df_get_all_workspaces = get_all_workspaces(header)
    # Set workspace list
    workspace_id_list = df_get_all_workspaces['id']
    # Define an empty dataframe
    df_get_all_report_users = pd.DataFrame()
    # Loop through workspace
    for workspace_id in workspace_id_list:
        workspace_name = df_get_all_workspaces.query('id == "{0}"'.format(workspace_id))["name"].iloc[0]
        # Define URL endpoint
        get_all_report_users_url =  f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}/users'
        # Send API call to get data
        result = requests.get(url=get_all_report_users_url, headers=header)
        # If result success then proceed:
        if result.status_code == 200:
            # Create dataframe to store data
            df = pd.DataFrame.from_dict(result.json()['value'], orient ='columns')
            # Add workspace name column
            df['workspaceName'] = workspace_name
            # Append data
            df_get_all_report_users = pd.concat([df_get_all_report_users,df])

    return df_get_all_report_users

def get_all_dataset_users(header,workspace_id,dataset_id):

    # Set workspace list
    df_get_all_workspaces = get_all_workspaces(header)
    # Set workspace list
    workspace_id_list = df_get_all_workspaces['id']
    # Define an empty dataframe
    df_get_all_dataset_users = pd.DataFrame()
    # Loop through workspace
    for workspace_id in workspace_id_list:
        workspace_name = df_get_all_workspaces.query('id == "{0}"'.format(workspace_id))["name"].iloc[0]
        # Define URL endpoint
        get_all_dataset_users_url =  f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/users'
        # Send API call to get data
        result = requests.get(url=get_all_dataset_users_url, headers=header)
        # If result success then proceed:
        if result.status_code == 200:
            # Create dataframe to store data
            df = pd.DataFrame.from_dict(result.json()['value'], orient ='columns')
            # Add workspace name column
            df['workspaceName'] = workspace_name
            # Append data
            df_get_all_dataset_users = pd.concat([df_get_all_dataset_users,df])

    return df_get_all_dataset_users

    
def update_parameter(header,workspace_id,dataset_id):

    data = {
        "updateDetails": [
            {
            "name": "DatabaseName",
            "newValue": "NewDB"
            },
            {
            "name": "MaxId",
            "newValue": "5678"
            }
        ]
    }
    # Define
    url = 'https://api.powerbi.com/v1.0/myorg/groups/{0}/datasets/{1}//Default.UpdateParameters'.format(workspace_id, dataset_id)
    
    # Send POST Request
    result = requests.post(url, headers= header, data= data)

    # Print Message
    print('Start updating parameter {0}'.format(dataset_id))