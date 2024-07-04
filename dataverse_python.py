import msal
import requests
import json
import logging


# Optional logging
# logging.basicConfig(level=logging.DEBUG)  # Enable DEBUG log for entire script
# logging.getLogger("msal").setLevel(logging.INFO)  # Optionally disable MSAL DEBUG logs

class DataversePython:
    def __init__(self, env_json: str, *args):
        self.session = None
        self.environment_uri: str = ""
        if 'xml' in args:
            self.filetype = 'xml'
        else:
            self.filetype = 'json'
        self.get_authenticated_session(env_json=env_json)

    def get_authenticated_session(self, env_json: str):
        config = json.load(open(env_json))

        self.environment_uri = config["environmentURI"]
        scope = [self.environment_uri + '/' + config["scopeSuffix"]]
        client_id = config["clientID"]
        authority = config["authorityBase"] + config["tenantID"]

        app = msal.PublicClientApplication(client_id, authority=authority)

        logging.info("Obtaining new token from AAD.")
        print("A local browser window will open for you to sign in. CTRL+C to cancel.")

        token = app.acquire_token_interactive(scope)

        if "access_token" in token:
            # Calling graph using the access token
            print("Token received successfully")
            session = requests.Session()
            session.headers.update(
                {
                    'Authorization': f'Bearer {token["access_token"]}',
                    'OData-MaxVersion': '4.0',
                    'OData-Version': '4.0',
                    'If-None-Match': 'null',
                    'Accept': f'application/{self.filetype}'
                }
            )

            self.session = session

        else:
            print(token("error"))
            print(token("error_description"))
            print(token("correlation_id"))

    def get_entity_set_names(self, schema_name):
        request_entities_uri = f'{self.environment_uri}api/data/v9.2/EntityDefinitions'
        response = self.session.get(request_entities_uri)

        if response.status_code != 200:
            print("Request failed. Error code:")
        else:
            print("Request successful")

        data = response.json()

        entities = [entity['SchemaName'] for entity in data['value']]
        if schema_name not in entities:
            print(f"{schema_name} not found")

        for entity in data['value']:
            if schema_name == entity['SchemaName']:
                print(f"Entity Set Name: {entity['EntitySetName']}")
                print(f"Logical Name: {entity['LogicalName']}")
                print(f"Primary Name Attribute: {entity['PrimaryNameAttribute']}")
                return entity['EntitySetName']

