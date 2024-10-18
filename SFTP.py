import paramiko
import logging


class SFTPClient:
    def __init__(self):
        self.client = ""
        self.pk_path = ""
        self.pk_password = ""
        self.being_used = False

    def connect(self, host, port, username, password):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=host, port=port, username=username, password=password)
            self.client = ssh_client.open_sftp()
            return "Success"

        except Exception as error:
            logging.basicConfig(filename='MonsterFTP.log', level=logging.ERROR, format='%(asctime)s - %(message)s')
            logging.error(f"FTP: {error}")
            return error

    def connect_with_key(self, host, port, username, password, pk_path, pk_pw):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            key = paramiko.RSAKey.from_private_key_file(pk_path, password=pk_pw)
            ssh_client.connect(hostname=host, port=port, username=username, password=password, pkey=key)
            self.client = ssh_client.open_sftp()
            return "Success"

        except Exception as error:
            logging.basicConfig(filename='MonsterFTP.log', level=logging.ERROR, format='%(asctime)s - %(message)s')
            logging.error(f"FTP: {error}")
            return error

    def set_private_key(self, path, password):
        self.pk_path = path
        self.pk_password = password
        return_list = [path, password]
        return return_list

