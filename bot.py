import uuid
from paramiko import SSHClient, paramiko


class Bot:
    def __init__(self, host:str, user:str, password:str):
        self.__client: SSHClient =  None

        self.id = str(uuid.uuid4())
        self.host = host
        self.user = user
        self.password = password


    def connect(self):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=self.user, password=self.password)


    def disconnect(self):
        self.client.close()


