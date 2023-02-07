import os
import ftplib
from datetime import datetime

NOW = datetime.now().strftime("%Y_%m_%d")
FPATH = "/opt/dump/"
LPATH = "/var/www/html/backup/"
RPATH = "html-site"
HOST = "12.54.98.11 2121"
USER = "user15"
PASSWD = "1o123923h827339fF3faucet3c9f681762686B02ef9a"

tmp_path = os.path.join(LPATH, 'tmp')
if not os.path.exists(tmp_path):
    os.makedirs(tmp_path)

files = []
for root, dirs, files_in_root in os.walk(LPATH):
    for file in files_in_root:
        if (file.endswith('.gz') or file.endswith('.tar')) and os.path.getmtime(os.path.join(root, file)) < (datetime.now() - datetime.timedelta(days=1)).timestamp():
            files.append(os.path.join(root, file))

for file in files:
    os.system(f'cp "{file}" {tmp_path}')

ftp = ftplib.FTP(HOST)
ftp.login(USER, PASSWD)
ftp.cwd(RPATH)
for file in files:
    ftp.storbinary(f'STOR {os.path.basename(file)}', open(os.path.join(tmp_path, os.path.basename(file)), 'rb'))
ftp.quit()

for file in files:
    os.remove(os.path.join(tmp_path, os.path.basename(file)))

print(f"{datetime.now().strftime('%d-%m-%Y %H:%M')} File transfer complete!")
