import re
import subprocess


class WIFI:
    def __init__(self):
        pass

    @staticmethod
    def get_wifi():
        try:
            data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], stderr=subprocess.PIPE,
                                           stdin=subprocess.PIPE, shell=True).decode(errors='ignore')
        except:
            return {}

        profiles = [wlan.strip() for wlan in re.findall(': (.*)', data)]

        res = []
        for wlan in profiles:
            try:
                p = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', wlan, 'key=clear'],
                                            stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            except:
                res.append({'Wi-Fi': wlan, 'Password': 'Not Found'})
                continue

            try:
                text_password = p.decode('cp866', errors='ignore')
                password = re.search('Содержимое ключа.*: (.*)\n', text_password).group(1).strip()
                res.append({'Wi-Fi': wlan, 'Password': password})
            except:
                try:
                    text_password = p.decode(errors='ignore')
                    password = re.search('Key Content.*: (.*)\n', text_password).group(1).strip()
                    res.append({'Wi-Fi': wlan, 'Password': password})
                except:
                    res.append({'Wi-Fi': wlan, 'Password': 'Not Found'})

        return {'Wi-Fi': res}


if __name__ == '__main__':
    pass
