import authenticate_with_msal
import json

# Parameters
path_to_environment_json = "env_iony_sandbox.json"

# Getting access token.
session, environment_uri = authenticate_with_msal.get_authenticated_session(path_to_environment_json, filetype=json)

EntityToDownload = "iony_recipes"

request_uri = f'{environment_uri}api/data/v9.2/{EntityToDownload}'

response = session.get(request_uri)

if response.status_code != 200:
    print("Request failed. Error code:")

else:
    print("Request successful")

data = response.json()

# Anzeige der Tabelleninformationen
for entity in data['value']:
    print(f"Recipe name: {entity['iony_name']}, Recipe type: {entity['crf4d_recipetype']}")

pass
