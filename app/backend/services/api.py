import requests

def fetch_csv_download_url(api_endpont):
    try:
        #send request for dataset information, including download link
        response = requests.get(api_endpont)

        #for bad responses
        response.raise_for_status()
        
        #convert from json
        data = response.json()

        #Process data here

        #grab the download url
        download_url = data['distribution'][0]['data']['downloadURL']
        #data title
        data_title = data['distribution'][0]['data']['title']
        #grab the date posted 
        date_issued = data['issued']
        #grab the date modified
        date_last_modified = data['modified']
        
        print("download url: ",download_url)
        print("data title: ",data_title)
        print("date issued: ",date_issued)
        print("date last modified: ",date_last_modified)
    except requests.RequestException as e:
        print(f"Error grabbing download information: {e}")

        