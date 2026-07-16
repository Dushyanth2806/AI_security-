import os
import json
import sys
import jsonschema

def validate_test_cases():
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema', 'test_case.schema.json')
    with open(schema_path) as f:
        schema = json.load(f)

    test_cases_dir = os.path.join(os.path.dirname(__file__), '..', 'test_cases')
    errors = []

    for root, _, files in os.walk(test_cases_dir):
        for file in files:
            if file.endswith(".json"):
                path = os.path.join(root, file)
                rel_dir = os.path.basename(root) # "injection" or "jailbreak"
                
                with open(path) as f:
                    try:
                        data = json.load(f)
                        jsonschema.validate(instance=data, schema=schema)
                        
                        expected_id = file[:-5]
                        if data.get("id") != expected_id:
                            errors.append(f"Error in {path}: id '{data.get('id')}' does not match filename '{expected_id}'")
                        
                        if data.get("category") != rel_dir:
                            errors.append(f"Error in {path}: category '{data.get('category')}' does not match directory '{rel_dir}'")
                            
                    except jsonschema.exceptions.ValidationError as e:
                        errors.append(f"Validation error in {path}: {e.message}")
                    except json.JSONDecodeError as e:
                        errors.append(f"JSON decode error in {path}: {e}")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
    else:
        print("All test cases validated successfully.")
        sys.exit(0)

if __name__ == "__main__":
    validate_test_cases()
