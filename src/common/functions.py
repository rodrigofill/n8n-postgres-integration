from datetime import datetime, timezone, timedelta
import uuid

from src.exceptions import ParamInvalid


def log_extra(individual_id, unique_id):
    return {"unique_id": unique_id, "individual_id": individual_id}


def uuid_4(is_ex=False):
    if is_ex:
        return uuid.uuid4().hex
    return str(uuid.uuid4())

def date_utc_now():
    return datetime.now(timezone.utc)

def date_brt_now():
    # Define the offset for São Paulo (UTC-3)
    sao_paulo_offset = timezone(timedelta(hours=-3))
    return datetime.now(sao_paulo_offset)

def date_now():
    return datetime.now().strftime("%Y-%m-%d")

def validate_param(field, value):
    if not value:
        raise ParamInvalid("Param {} {} is invalid!".format(field, value))

def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
    except:
        raise ParamInvalid("Param with value '{}' is invalid!".format(date_string))
