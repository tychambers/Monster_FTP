from ftplib import FTP
import socket
import psycopg2
from FTP import Client
import sys
import logging
from MessageBox import pop_up
import paramiko
import os
from SFTP import SFTPClient
from ClientConnectionBox import client_connect_box
import pandas as pd


conn = psycopg2.connect(host="localhost", dbname="ftpdb", user="postgres",
                        password="Admin123!!!", port=5432)
cur = conn.cursor()
query = '''
CREATE TABLE IF NOT EXISTS transactions (
protocol VARCHAR(255) NOT NULL,
transaction_type VARCHAR(255) NOT NULL,
source_path VARCHAR(255) NOT NULL,
dest_path VARCHAR(255) NOT NULL,
time VARCHAR(255) NOT NULL
)'''
# query2 = '''
# INSERT INTO transactions (transaction_type, source_path, dest_path, time)
# VALUES('test','test', 'test', 'test')
# '''
new_query = '''
SELECT * FROM transactions'''

cur.execute(new_query)

results = cur.fetchall()
df = pd.DataFrame(results, columns=[desc[0] for desc in cur.description])
df.to_csv("your_output_file.csv", index=False)

cur.close()
conn.close()


# ssh_client = paramiko.SSHClient()
# ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # key_path = "C:/ProgramData/Globalscape/EFT Server/testkey"
# key_path = ""
# key = paramiko.RSAKey.from_private_key_file(key_path, password="")
# test = ssh_client.connect(hostname="localhost", port=22, username="user1", password="a", pkey=key)
# client = ssh_client.open_sftp()
# client.chdir("test_folder")
# x = client.getcwd()
# print(test)
# ftpclient = Client()
# sftpclient = SFTPClient()
#
# client_connect_box(ftpclient, sftpclient)


# ftp_client = FTP()
# ftp_client.connect(host="localhost", port=21)
# ftp_client.login(user="user1", passwd="a")
# test = ftp_client.nlst()
# test1 = ftp_client.pwd()
# # the name of file you want to download from the FTP server
# # local_path = "C:/test/test1.txt"
# # filename = "test1.txt"
# # with open(local_path, "wb") as file:
# #     # use FTP's RETR command to download the file
# #     ftp_client.retrbinary(f"RETR {filename}", file.write)
#
# print(test1)

# ssh_client = paramiko.SSHClient()
# ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh_client.connect(hostname="localhost", port=22, username="user1", password="a")
# client = ssh_client.open_sftp()
# client.chdir("test_folder")
# test = client.getcwd()
# print(test)

