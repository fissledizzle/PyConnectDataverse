import authenticate_with_msal
from requests.utils import get_encoding_from_headers

# Parameters
path_to_environment_json = "env_iony_sandbox.json"

# Getting access token.
session, environment_uri = authenticate_with_msal.get_authenticated_session(path_to_environment_json, filetype="xml")
# Metadata XML
request_service_docs_uri = f'{environment_uri}api/data/v9.2/$metadata'

response = session.get(request_service_docs_uri)
if response.status_code != 200:
    print("Request failed. Error code:")
    raw = response.content.decode('utf-8')
    print(raw)
else:
    print("Connection successful")
    print(response.headers["content-type"])
    with open('metadata.xml', 'w') as f:
        response.encoding = "utf-8"
        f.write(response.text)

