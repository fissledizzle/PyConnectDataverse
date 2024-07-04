import pandas as pd
import authenticate_with_msal

# Parameters
path_to_environment_json = "env_iony_sandbox.json"
data_to_write = 'data\M to N.csv'
EntityM = 'systemusers'
EntityN = 'teams'
m_to_n_relationship = 'teammembership_association'
# Column names in CSV must match EntityM and EntityN above

# Getting access token.
session, environment_uri = authenticate_with_msal.get_authenticated_session(path_to_environment_json)

# reading the CSV
df = pd.read_csv(data_to_write)

successful_updates = 0
failures = 0
expected_updates = len(df)

for index, row in df.iterrows():
    record_m = row[EntityM]
    record_n = row[EntityN]

    request_uri = f'{environment_uri}api/data/v9.2/{EntityM}({record_m})/{m_to_n_relationship}/$ref'
    odata_id = f'{environment_uri}api/data/v9.2/{EntityN}({record_n})'
    post_json = {"@odata.id": odata_id}

    response = session.post(request_uri, json=post_json)

    if response.status_code != 204:
        failures += 1
        raw = response.content.decode('utf-8')
        print(f'Error linking {record_m} to {record_n}. Error {response.status_code}: \n{raw}\n')

    else:
        successful_updates += 1

    if index % 10 == 0:
        print(f"Processed: {index + 1}")

print(f'{successful_updates} UPDATES MADE OF {expected_updates} EXPECTED UPDATES.\n{failures} FAILURES.')
