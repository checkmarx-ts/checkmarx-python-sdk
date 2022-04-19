# encoding: utf-8
def get_url_param(url_param_key, value):
    """

    Args:
        url_param_key (str):
        value (`list` of str, str):

    Returns:
        str
    """
    result = ""
    if not value:
        return result
    if isinstance(value, str):
        result += "&{param_key}={pram_value}".format(param_key=url_param_key, pram_value=value)
    elif isinstance(value, (list, tuple)):
        for item in value:
            if not item:
                continue
            result += "&{param_key}={pram_value}".format(param_key=url_param_key, pram_value=str(item))
    return result


def type_check(param, param_type):
    """

    Args:
        param :
        param_type :

    Raises:
        ValueError
    """
    if param is None:
        return
    if isinstance(param_type, tuple):
        type_true = False
        for item_type in param_type:
            type_true = type_true or isinstance(param, item_type)
        if not type_true:
            raise ValueError("Error, parameter type should be {type}".format(type=str(param_type)))
    if not isinstance(param, param_type):
        raise ValueError("Error, parameter type should be {type}".format(type=str(param_type)))


def list_member_type_check(list_param, member_type):
    if not list_param:
        return
    for item in list_param:
        type_check(item, member_type)


def int_range_check(param, start_range, end_range):
    if param and param not in range(start_range, end_range):
        raise ValueError(("Error, parameter out of range, "
                          "minimum value={min}, maximum value={max}").format(
            min=start_range, max=end_range - 1
        ))
