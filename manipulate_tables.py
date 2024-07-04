import authenticate_with_msal
import json
from dataverse_python import DataversePython


dataverse = DataversePython(env_json="env_iony_sandbox.json")

dataverse.get_entity_set_names(schema_name='crf4d_Fabricates')
