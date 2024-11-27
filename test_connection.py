import authenticate_with_msal
from requests.utils import get_encoding_from_headers

# Parameters
data_to_write = "iony_sandbox.json"


# a test request to the URI to get data
session, environment_uri = authenticate_with_msal.get_authenticated_session(data_to_write, filetype="json")

request_uri = f'{environment_uri}api/data/v9.2/'
response = session.get(request_uri)

if response.status_code != 200:
    print("Request failed. Error code:")
    raw = response.content.decode('utf-8')
    print(raw)

else:
    print("Connection successful")
    content = response.json()
    for key, value in content.items():
        print(f"{key}: {value}")
