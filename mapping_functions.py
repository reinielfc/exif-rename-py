import re
from datetime import datetime
from unicodedata import normalize

import pytz as pytz
from caseconverter import *


def detox(string: str) -> str:
    detoxed_string = (normalize('NFKD', string)
                      .encode('ascii', 'ignore')
                      .decode('ascii'))

    return re.sub(r"[^\s0-9A-Za-z._-]", '_', detoxed_string)


def standardize_date(date_string: str, input_format: str = "%Y:%m:%d %H:%M:%S") -> str:
    return datetime.strptime(date_string, input_format).isoformat()


def add_timezone(date_string: str, timezone: str = "US/Eastern") -> str:
    dt = datetime.fromisoformat(date_string)
    dt = pytz.timezone(timezone).localize(dt)
    return str(dt)


def date_to_epoch(date_string: str) -> str:
    return str(datetime.fromisoformat(date_string).timestamp())


_function_dict = {
    "capitalize": str.capitalize,
    "title": str.title,
    "fold": str.casefold,
    "lower": str.lower,
    "swap": str.swapcase,
    "upper": str.upper,
    "detox": detox,
    "date": standardize_date,
    "tz": add_timezone,
    "epoch": date_to_epoch,
    "int": lambda string: str(int(float(string))),
    "camel": lambda string: camelcase(string),
    "cobol": lambda string: cobolcase(string),
    "flat": lambda string: flatcase(string),
    "kebab": lambda string: kebabcase(string),
    "macro": lambda string: macrocase(string),
    "pascal": lambda string: pascalcase(string),
    "snake": lambda string: snakecase(string),
    # 2+ args
    "prefix": lambda string, prefix: prefix + string,
    "suffix": lambda string, suffix: string + suffix,
    "replace": lambda string, old, new, count=-1: string.replace(old, new, int(count)),
}


def apply_function(function_name: str, *args):
    function = _function_dict.get(function_name)

    if function is None:
        raise RuntimeError(f'function by name "{function_name}" not found')

    return function(*args)
