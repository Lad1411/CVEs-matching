import json

def read_content(file_path):
    """
        Read content from .txt file

        Args:
            content: str contains information of that file
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return content


def to_native_python(obj):
    if hasattr(obj, 'items'):  # Handles MapComposite
        return {k: to_native_python(v) for k, v in obj.items()}
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):  # Handles RepeatedComposite
        return [to_native_python(v) for v in obj]
    return obj

def save_result_to_file(result, output_file):
    """
        Save result to json file

        Args:
            result: Result
            output_file: save result to this file
    """
    with open(output_file, 'w') as file:

        # Convert the protobuf object to a standard dict
        clean_data = to_native_python(result)
        data = json.dumps(clean_data, indent=4)

        file.write(data)
        print('Save file successfully')