import get_token
import requests

def refresh_dataset(workspace_id,dataset_id):

    access_token = get_token()

    header = {
    'Content-Type':'application/json', 
    'Authorization':f'Bearer {access_token}'
    }

    url = 'https://api.powerbi.com/v1.0/myorg/groups/{0}/datasets/{1}/refreshes'.format(workspace_id, dataset_id)
    result = requests.post(url, headers= header)

    # Refresh dataset
    print('Start refreshing dataset {0}'.format(dataset_id))
    