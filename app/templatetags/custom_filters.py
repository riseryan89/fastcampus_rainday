from django import template


register = template.Library()


@register.filter()
def wind_direction(value):
    if value == "0":
        return "-"
    elif value == "360":
        return "N"
    elif value == "20":
        return "NNE"
    elif value == "50":
        return "NE"
    elif value == "70":
        return "ENE"
    elif value == "90":
        return "E"
    elif value == "110":
        return "ESE"
    elif value == "140":
        return "SE"
    elif value == "160":
        return "SSE"
    elif value == "180":
        return "S"
    elif value == "200":
        return "SSW"
    elif value == "230":
        return "SW"
    elif value == "250":
        return "WSW"
    elif value == "270":
        return "W"
    elif value == "290":
        return "WNW"
    elif value == "320":
        return "NW"
    else:
        return value
