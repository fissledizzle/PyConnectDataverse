import pandas as pd
import authenticate_with_msal
import json

# Parameters
path_to_environment_json = "env_iony_sandbox.json"
target_table = "iony_recipes"
path_to_csv_of_records = "data\pcd_update_records.csv"
# Column names in CSV must match EntityM and EntityN above

# Getting access token.
session, environment_uri = authenticate_with_msal.get_authenticated_session(path_to_environment_json, filetype='json')

session.headers.update({'If-Match': '*'})

# reading the CSV
df = pd.read_csv(path_to_csv_of_records)
records = json.loads(df.drop(columns='GUID').to_json(orient="records"))

successful_updates = 0
failures = 0
expected_updates = len(df)

for index, row in df.iterrows():

    guid = row['GUID']
    request_uri = f'{environment_uri}api/data/v9.2/{target_table}({guid})'
    post_json = records[index]

    response = session.patch(request_uri, json=post_json)

    if response.status_code != 204:
        failures += 1
        raw = response.content.decode('utf-8')
        print(f'Error updating {guid}. Error {response.status_code}: \n{raw}\n')

    else:
        successful_updates += 1

    if index % 10 == 0:
        print(f"Processed: {index + 1}")

print(f'{successful_updates} UPDATES MADE OF {expected_updates} EXPECTED UPDATES.\n{failures} FAILURES.')
