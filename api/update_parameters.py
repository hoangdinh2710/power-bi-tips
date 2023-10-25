import get_token
import requests

def update_parameter(workspace_id,dataset_id):

    access_token = get_token()

    header = {
    'Content-Type':'application/json', 
    'Authorization':f'Bearer {access_token}'
    }

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

    url = 'https://api.powerbi.com/v1.0/myorg/groups/{0}/datasets/{1}//Default.UpdateParameters'.format(workspace_id, dataset_id)
    result = requests.post(url, headers= header, data= data)

    # Refresh dataflow
    print('Start updating parameter {0}'.format(dataset_id))
    