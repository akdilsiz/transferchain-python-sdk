import uuid
from datetime import datetime


def datetime_formating(date_str, format='%Y-%m-%dT%H:%M:%S.%fZ'):
    """
    String datetime to datetime object

    Parameters:
        date_str (str):
            string datetime

        format (str):
            datetime format. optional

    Returns:
        Datetime object

    Example:
        -
    ```
        from transferchain import utils
        result = utils.datetime_formating('2023-09-21T09:07:57.620532Z')

    ```
    """
    return datetime.strptime(date_str, format)


def datetime_to_str(date_obj, format='%Y-%m-%dT%H:%M:%SZ'):
    """
    Datetime to string

    Parameters:
        date_obj (str):
            datetime object

        format (str):
            datetime format. optional

    Returns:
        String datetime

    Example:
        -
    ```
        import datetime
        from transferchain import utils
        date_obj = utils.datetime_formating('2023-09-21T09:07:57.620532Z')
        result = utils.datetime_to_str(date_obj)
    ```
    """
    return date_obj.strftime(format)


def is_valid_uuid(val):
    """
    UUId validation

    Parameters:
        val (str):
            uuid string

    Returns:
        Boolean

    Example:
        -
    ```
        import datetime
        from transferchain import utils
        result = utils.is_valid_uuid(str(uuid.uuid4()))
    ```
    """
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
