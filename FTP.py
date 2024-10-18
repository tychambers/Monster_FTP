from ftplib import FTP
import logging


class Client:
    def __init__(self):
        self.client = ""

    def connect(self, host, port, username, password):
        ftp_client = FTP()

        try:
            ftp_client.connect(host=host, port=port)
            ftp_client.login(user=username, passwd=password)
            self.client = ftp_client
            return "Success"

        except Exception as error:
            logging.basicConfig(filename='MonsterFTP.log', level=logging.ERROR, format='%(asctime)s - %(message)s')
            logging.error(f"FTP: {error}")
            return error
