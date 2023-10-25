import get_token
import requests

def refresh_dataflow(workspace_id,dataflow_id):

    access_token = get_token()

    header = {
    'Content-Type':'application/json', 
    'Authorization':f'Bearer {access_token}'
    }

    url = 'https://api.powerbi.com/v1.0/myorg/groups/{0}/dataflows/{1}/refreshes'.format(workspace_id, dataflow_id)
    result = requests.post(url, headers= header)

    # Refresh dataflow
    print('Start refreshing dataflow {0}'.format(dataflow_id))
    