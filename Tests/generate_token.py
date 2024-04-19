# import json

# # def generate_token(username, email, password):
    
# #     return "example_token"

# def load_json_schema(schema_file):
#     with open(schema_file, "r") as file:
#         return json.load(file)

# if __name__ == "__main__":
#     schema = load_json_schema("task_schema.json")
#     print("Loaded JSON Schema:")
#     print(schema)

import json
from jsonschema import validate, ValidationError
 
def validate_task_schema(response_data, schema_file):
    # Decode the response data from bytes to string
    response_data_str = response_data.decode('utf-8')
   
    # Load the schema from the schema file
    with open(schema_file) as f:
        schema = json.load(f)
   
    try:
        # Parse the response data as JSON
        response_json = json.loads(response_data_str)
       
        # Validate the response JSON against the schema
        validate(instance=response_json, schema=schema)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"Failed to decode JSON: {str(e)}"
    except ValidationError as e:
        return False, f"Response does not match the schema: {str(e)}"