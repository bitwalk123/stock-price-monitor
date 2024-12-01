class LoginInfo:
    def __init__(self, login_info: dict):
        self.login_info = login_info

    def getLoginID(self) -> str:
        return self.login_info['loginid']

    def getPassword(self) -> str:
        return self.login_info['password']

    def getPassnumber(self) -> str:
        return self.login_info['passnumber']
