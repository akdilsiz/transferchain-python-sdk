import uuid
from datetime import datetime


def datetime_formating(date_str, format='%Y-%m-%dT%H:%M:%S.%fZ'):
    return datetime.strptime(date_str, format)


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
