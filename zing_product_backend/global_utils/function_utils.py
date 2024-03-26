def find_values_by_key(data, target_key, found_values=None):
    if found_values is None:
        found_values = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                found_values.append(value)
            else:
                find_values_by_key(value, target_key, found_values)
    elif isinstance(data, list):
        for item in data:
            find_values_by_key(item, target_key, found_values)
    return found_values

