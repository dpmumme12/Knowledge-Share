from django import template
from datetime import datetime

register = template.Library()


@register.filter
def date_time(datetime_str: str, args: str) -> str:
    """
    Takes in a datetime string, the current format of that date time
    converts it to a datetime object and outs the date time witht he new format.
    Example usage:
    {{12/06/2021 09:15:32|date_time:"%m/%d/%Y %H:%M:%S~%f~%d/%m/%Y"}}
    Outputs: 06/12/2021

    The two arguments are separated with the "~" symbol.
    First arument is the current format of the date time string.
    Second argument is the desired format.

    See datetime docs below for format string codes.
    https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    """
    _params = args.split('~')
    current_format = _params[0]
    new_format = _params[1]
    d = datetime.strptime(datetime_str, current_format)
    return d.strftime(new_format)
