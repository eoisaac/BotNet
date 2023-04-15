import argparse


class BotNet:
    def __init__(self, host: str = '', user: str = '', pwd_src_path: str = ''):
        self.host = host
        self.user = user
        self.pwd_src_path = pwd_src_path
        self.__get_args()

    def __get_args(self):
        parser = argparse.ArgumentParser(description='Zip file password cracker')
        parser.add_argument('-H', dest='host', type=str, help='Target host', required=True)
        parser.add_argument('-u', dest='user', type=str, help='Target user', required=True)
        parser.add_argument('-F', dest='pwd_src_path', type=str, help='Passwords source path', required=True)
        args = parser.parse_args()

        self.host = args.host
        self.user = args.user
        self.pwd_src_path = args.pwd_src_path



botnet = BotNet()
print(botnet.host)
print(botnet.user)
print(botnet.pwd_src_path)

