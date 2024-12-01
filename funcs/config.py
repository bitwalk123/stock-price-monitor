import os

from funcs.common import read_json
from structs.login_info import LoginInfo
from structs.web_info import WebInfoRakuten


def get_login_info(info: WebInfoRakuten) -> LoginInfo:
    """Get login information

    :return:
    """
    conf_login = 'login.json'
    dir = info.getConfigDir()
    file_json = os.path.join(dir, conf_login)
    return set_json2obj(file_json)


def set_json2obj(file_json) -> LoginInfo:
    """Set login information to LoginInfo object

    :param file_json:
    :return:
    """
    dict_info = read_json(file_json)
    obj_login = LoginInfo(dict_info)
    return obj_login
