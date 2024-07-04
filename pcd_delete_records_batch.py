import authenticate_with_msal
import json
import pandas as pd
import time
import uuid
from requests import Request

# Parameters
path_to_environment_json = "example-env_iony_sandbox.json"
target_table = "contacts"
data_to_write = "data\pcd_delete_records.csv"
batch_size = 950

# Getting access token.
session, environment_uri = authenticate_with_msal.get_authenticated_session(path_to_environment_json)

# choose how you would like to act on errors
session.headers.update({"Prefer": "odata.continue-on-error"})

# the post uri
batch_uri = f'{environment_uri}api/data/v9.2/$batch'
request_uri = f'/api/data/v9.2/{target_table}'

# read the CSV and convert to dataframe
df = pd.read_csv(data_to_write)

first = 0
last = batch_size - 1

result_df = df.copy()
result_df['codes'] = ""
result_df['messages'] = ""
result_df['batch'] = ""

timeStart = time.perf_counter()

while first < len(df.index):
    boundary = f"batch_{str(uuid.uuid4())}"
    session.headers.update({"Content-Type": f'multipart/mixed; boundary="{boundary}"'})
    boundary = "--" + boundary

    requestdf = df.loc[first:last]
    body = ""

    records = json.loads(requestdf.drop(columns='GUID').to_json(orient="records"))

    for index, row in requestdf.iterrows():
        guid = row['GUID']

        request = boundary + """
Content-Type: application/http
Content-Transfer-Encoding: binary

DELETE """ + request_uri + "(" + guid + ")" + """ HTTP/1.1
Content-Type: application/json

"""

        body = body + request

    body = (body + "\n" + boundary + "--").encode()

    req = Request(
        'POST',
        batch_uri,
        data=body,
        headers=session.headers
    ).prepare()

    r = session.send(req)

    response = r.content.decode('utf-8')
    delimiter = response[0:52]

    responses = response.split(delimiter)

    codes = []
    messages = []

    for i in range(1, len(responses) - 1):
        responses[i] = responses[i].removeprefix(
            "\r\nContent-Type: application/http\r\nContent-Transfer-Encoding: binary\r\n\r\nHTTP/1.1 ")
        responses[i] = responses[i].split('\r\n', 1)
        codes.append(responses[i][0])
        messages.append(responses[i][1])
        i += 1

    result_df.loc[first:last, 'codes'] = codes
    result_df.loc[first:last, 'messages'] = messages
    result_df.loc[first:last, 'batch'] = boundary

    result_df.loc[first:last].to_csv(f"output\{boundary}.csv")

    successes = sum(1 for i in codes if i == "204 No Content")
    sent = len(requestdf.index)

    print(f"Records {first} : {last} sent for import. {sent - successes} failures.")

    first = last + 1
    last = min(last + batch_size, len(df.index))

print(f'IMPORTING TOOK: {round(time.perf_counter() - timeStart, 0)} SECONDS ')
result_df.to_csv("output\changes.csv")
