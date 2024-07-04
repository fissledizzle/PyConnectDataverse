import authenticate_with_msal
import json
import pandas as pd
import time
from requests import Request, Session

# HowTo https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/create-entity-web-api

# Parameters
path_to_environment_json = "env_iony_sandbox.json"
session, environment_uri = authenticate_with_msal.get_authenticated_session(path_to_environment_json, filetype='json')

record1 = {"crf4d_fcode": "F3",
           "crf4d_PrimaryContactId":
               {
                   "firstname": "John3",
                   "lastname": "Smith3"
               }
           }

record2 = {"name": "Sample Account4",
           "primarycontactid":
               {
                   "firstname": "John4",
                   "lastname": "Smith4"
               }
           }

target_table = 'crf4d_fabricateses'
request_uri = f'{environment_uri}api/data/v9.2/{target_table}'

req = Request('POST', request_uri, json=record1, headers=session.headers).prepare()
response = session.send(req)

print(f"Status code: {response.status_code}")
