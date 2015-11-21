def integer_field(value, name):
    if type(value) != int:
        raise ValueError("Value '{}' for field '{}' is not a valid integer.".format(value, name))
    return value


def float_field(value, name):
    if type(value) != float:
        raise ValueError("Value '{}' for field '{}' is not a valid float.".format(value, name))
    return value
