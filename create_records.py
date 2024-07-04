import authenticate_with_msal
import json
import pandas as pd
import time
from requests import Request, Session

# HowTo https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/create-entity-web-api

# Parameters
path_to_environment_json = "env_iony_sandbox.json"
target_table = "iony_recipes"
data_to_write = "data\pcd_create_records.csv"
attributes_to_return = "?$select=iony_name"  # optionally include the attributes to return, otherwise all are returned

# The Pandas data types of the columns imported to avoid import issues
dtypes = {
    "iony_name": "object",
    "crf4d_recipetype": "object"
}

# read the CSV and convert to dataframe
df = pd.read_csv(data_to_write, dtype=dtypes)

records = json.loads(df.to_json(orient="records"))


# Getting access token.
session, environment_uri = authenticate_with_msal.get_authenticated_session(path_to_environment_json, filetype='json')
session.headers.update({"Prefer": "return=representation"})  #

# the post uri
request_uri = f'{environment_uri}api/data/v9.2/{target_table}{attributes_to_return}'

row = 0
successful_updates = 0
failures = 0
expected_updates = len(df)
percent_complete = 0
timeStart = time.perf_counter()

for record in records:
    req = Request('POST', request_uri, json=record, headers=session.headers).prepare()
    response = session.send(req)
    record['HTTP_RESPONSE'] = response.status_code
    record['HTTP_CONTENT'] = json.loads(response.content.decode('utf-8'))

    if response.status_code != 201:
        failures += 1

    else:
        successful_updates += 1

    row += 1
    if round(row / expected_updates * 100, 0) != percent_complete:
        percent_complete = round(row / expected_updates * 100, 0)
        print(f"{percent_complete}% complete")

print(f'{successful_updates} UPDATES MADE OF {expected_updates} EXPECTED UPDATES. {failures} FAILURES.')
print(f'IMPORTING TOOK: {round(time.perf_counter() - timeStart, 0)} SECONDS ')

