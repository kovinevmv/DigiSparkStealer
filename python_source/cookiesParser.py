import json


class CookiesParses:
    def __init__(self, _filename, _data):
        self.filename = _filename
        self.data = _data

        self.cookie_file = open(self.filename, 'w')

        if self.data:
            self.write_data()

    def write_data(self):
        for browser, cookies in self.data.items():
            if browser:
                for url, cookie in cookies.items():
                    self.cookie_file.write('Browser: ' + browser + '\nSite: ' + url + '\n')
                    self.cookie_file.write(json.dumps(cookie) + '\n')
                    self.cookie_file.write("-----------------------------------\n")
        self.cookie_file.close()


if __name__ == '__main__':
    pass
