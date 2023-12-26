import uuid

def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.
    """
    try:
        uuid_obj = uuid.UUID(str(uuid_to_test), version=version)
        return str(uuid_obj) == str(uuid_to_test)
    except ValueError:
        return False