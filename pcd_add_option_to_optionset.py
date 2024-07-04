import pandas as pd
import authenticate_with_msal

# Parameters
path_to_environment_json = "example-env_iony_sandbox.json"
data_to_write = "data\OptionsToAdd.csv"
value_of_first_added_option = 201300004
option_set_logical_name = "OPTION SET NAME"
language_code = 1033
unique_solution_name = "SOLUTION NAME"

# Getting access token.
session, environment_uri = authenticate_with_msal.get_authenticated_session(path_to_environment_json)

# reading the CSV
df = pd.read_csv(data_to_write)

successful_updates = 0
expected_updates = len(df)

request_uri = f'{environment_uri}api/data/v9.2/InsertOptionValue'

print("Adding...")

for index, row in df.iterrows():
    label = row["Label"]
    color = row["Color"]
    
    post_json = {
                "OptionSetName": option_set_logical_name,
                "Value": value_of_first_added_option,
                "Color": color,
                "Label": {
                    "@odata.type": "Microsoft.Dynamics.CRM.Label",
                    "LocalizedLabels": [
                    {
                        "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                        "Label": label,
                        "LanguageCode": language_code,
                        "IsManaged": 'false'
                    }
                    ],
                    "UserLocalizedLabel": {
                        "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                        "Label": label,
                        "LanguageCode": language_code,
                        "IsManaged": 'false'
                    }
                },
                "SolutionUniqueName": unique_solution_name
                }

    r = session.post(request_uri, json = post_json)

    if r.status_code != 200:
        raw = r.content.decode('utf-8')
        print(raw)
        break

    else:
        print(label)
        successful_updates += 1
        value_of_first_added_option += 1

print(f'{successful_updates} UPDATES MADE OF {expected_updates} EXPECTED UPDATES') 