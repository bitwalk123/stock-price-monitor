from funcs.common import read_json
from structs.login_info import LoginInfo


def get_login_info() -> LoginInfo:
    """Get login information

    :return:
    """
    file_json = 'login.json'
    return set_json2obj(file_json)


def set_json2obj(file_json) -> LoginInfo:
    """Set login information to LoginInfo object

    :param file_json:
    :return:
    """
    dict_info = read_json(file_json)
    obj_login = LoginInfo(dict_info)
    return obj_login
