# Great thanks to the sources I gathered some code from:
# - http://radtek.ca/blog/delete-old-email-messages-programatically-using-python-imaplib/
# - https://stackoverflow.com/questions/6225763/downloading-multiple-attachments-using-imaplib
# - https://stackoverflow.com/questions/43857002/script-in-python-to-download-email-attachments

import imaplib, datetime, random, email, os, configparser, time, requests, json
from webdav3.client import Client
from os import listdir
from os.path import isfile, join
from pathlib import Path

#os.chdir("/opt/app")

config = configparser.ConfigParser()
config.read('settings.ini')


class Dav:
    """A class to handle webdav request for uploading the mail attachments
    """
    def __init__(self, host, user, password):
        """initializes a webdav connection

        Args:
            host (string): host url
            user (string): dav user name
            password (string): dav password
        """

        self.options = {
        'webdav_hostname': host,
        'webdav_login':    user,
        'webdav_password': password
        }
        self.client=Client(self.options)

    def uploadAll(self, local_dir, upload_dir):
        """Uploads all attachments to the cloud

        Args:
            dir (string): existing directory to save the files to

        Returns:
            False: if something went wrong
        """
        for p in Path(local_dir).rglob( '*' ):
            try:
                upload_path = join(upload_dir, p)
                if self.client.check(remote_path=upload_path):
                    upload_path = upload_path.with_name(upload_path.stem + '_' +str(random.randint(10000,100000))+ upload_path.suffix)
                self.client.upload_sync(remote_path=upload_path, local_path=join(local_dir, p))
                os.remove("attachments/"+f)
            except Exception as e:
                print(f"failed uploading file {p} with: {e}")


d = Dav(config['dav']['host'], config['dav']['user'], config['dav']['password'])
last = datetime.datetime.now()-datetime.timedelta(days=1)

while True:
    if datetime.datetime.now()-last > datetime.timedelta(minutes=2):
        print("run")
        last = datetime.datetime.now()
        try:
            d.uploadAll(config['files']['folder'], config['dav']['save_path'])
        except Exception as e:
            print(f"loop failed with {e}")
            d = Dav(config['dav']['host'], config['dav']['user'], config['dav']['password'])
        time.sleep(120)


