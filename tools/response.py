def assert_dict_struct(data, structure):
    print("data", data)
    print("structure", structure)
    if isinstance(structure, dict):
        assert isinstance(data, dict)
        for key, value in structure.items():
            assert key in data
            assert_dict_struct(data[key], value)
    elif isinstance(structure, list):
        assert isinstance(data, list)
        for item in data:
            assert_dict_struct(item, structure[0])
    else:
        isinstance(data, structure)


def has_error_status(result: dict) -> bool:
    return result["result"]["status"] == "error"


def has_success_status(result: dict) -> bool:
    return result["result"]["status"] == "success"


def has_message(result: dict) -> bool:
    return "message" in result["result"]


def has_data(result: dict) -> bool:
    return "data" in result["result"]


def message_is(result: dict, message: dict) -> bool:
    return result["result"]["message"] == message


def data_is(result: dict, data: dict) -> bool:
    return result["result"]["data"] == data


def message_contains(result: dict, message: dict) -> bool:
    return message in result["result"]["message"]


def data_contains(result: dict, data: dict) -> bool:
    return data in result["result"]["data"]
