# Great thanks to the sources I gathered some code from:
# - http://radtek.ca/blog/delete-old-email-messages-programatically-using-python-imaplib/
# - https://stackoverflow.com/questions/6225763/downloading-multiple-attachments-using-imaplib
# - https://stackoverflow.com/questions/43857002/script-in-python-to-download-email-attachments

import datetime, random, os, configparser, time
from webdav3.client import Client
from os.path import join, abspath, relpath, isdir
from pathlib import Path


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
        local_dir_abs = abspath(local_dir)

        for p in Path(local_dir_abs).rglob( '*' ):
            if isdir(p):
                continue

            p = relpath(p, local_dir_abs)
            try:
                upload_path = Path(join(upload_dir, p))
                if self.client.check(remote_path=str(upload_path)):
                    upload_path = upload_path.with_name(upload_path.stem + "_" +str(random.randint(10000,100000))+ upload_path.suffix)
                self.client.upload_sync(remote_path=str(upload_path), local_path=join(local_dir_abs, p))
                os.remove(join(local_dir_abs, p))
            except Exception as e:
                print(f"failed uploading file {p} with: {e}")


d = Dav(config['dav']['host'], config['dav']['user'], config['dav']['password'])
last = datetime.datetime.now()-datetime.timedelta(days=1)

while True:
    if datetime.datetime.now()-last > datetime.timedelta(minutes=1):
        print("run")
        last = datetime.datetime.now()
        try:
            d.uploadAll(config['files']['folder'], config['dav']['save_path'])
        except Exception as e:
            print(f"loop failed with {e}")
            d = Dav(config['dav']['host'], config['dav']['user'], config['dav']['password'])
        time.sleep(60)


