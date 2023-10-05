import datetime


def serialize_datetime(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def deserialize_datetime(entry_dict: dict):
    if "release_date" in entry_dict:
        entry_dict["release_date"] = datetime.date.fromisoformat(entry_dict["release_date"])
    return entry_dict
