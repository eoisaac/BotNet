import uuid
import paramiko


class Bot:
    def __init__(self, host:str, user:str, password:str):
        self.__client: paramiko.SSHClient =  None

        self.id = str(uuid.uuid4())
        self.name = ''
        self.host = host
        self.user = user
        self.password = password


    def execute_command(self, command: str):
        stdin, stdout, stderr = self.__client.exec_command(command)
        return stdout.read().decode('utf-8')


    def connect(self) -> bool:
        try:
            self.__client = paramiko.SSHClient()
            self.__client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.__client.connect(self.host, username=self.user, password=self.password)

            bot_name = self.execute_command('whoami').replace('\n', '')
            self.name = f'{self.user}@{bot_name}'
            return True
        except:
            if self.__client:
                self.__client.close()
            return False


    def disconnect(self):
        self.__client.close()


