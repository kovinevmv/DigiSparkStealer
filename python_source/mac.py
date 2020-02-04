import re
import subprocess


class Mac:
    """
    Class Mac allows you to extract all wireless lan adapter mac-addresses.
    Class parse output of 'ipconfig /all'. To get all addresses, you could
    use a special function 'getmac', but it runs longer 3 times than the ifconfig
    Example of get_mac() result:
    {
        'Mac-Address':
        [
            {'Interface': 'Intel Dual Band', 'Mac-Address': '12:34:56:78:9A:BC'},
            {'Interface': 'VirtualBox Adapter', 'Mac-Address': '12:34:56:78:9A:BD'},
        ]
    }
    """
    def __init__(self):
        pass

    def get_mac(self):
        """ Parse ipconfig /all and return dict. """
        macs_parsed = {}

        # Try to run subprocess and decode output with cp866 or utf-8
        try:
            ipconfig_res = subprocess.check_output('ipconfig /all', stderr=subprocess.PIPE,
                                                   stdin=subprocess.PIPE, shell=True).decode('cp866').strip()
        except:
            try:
                ipconfig_res = subprocess.check_output('ipconfig /all', stderr=subprocess.PIPE,
                                                   stdin=subprocess.PIPE, shell=True).decode().strip()
            except:
                return {}

        # Find macs by regex and add to dict
        try:
            p = re.compile(': (.*)\n\r?.*: ((?:[A-Fa-f0-9]{2}-){5}(?:[A-Fa-f0-9]{2})(?!-))')
            name_and_mac = re.findall(p, ipconfig_res)
            macs_parsed['Mac-Address'] = [{'Interface': name.replace('\r', ''),
                                           'Mac-Address': mac.replace('-', ':')}
                                          for name, mac in name_and_mac]

        # Error to parse output, write all output
        except Exception as e:
            macs_parsed['Mac-Address'] = [{'Error to parse': str(e), 'Data': ipconfig_res}]
            return macs_parsed

        return macs_parsed


if __name__ == '__main__':
    pass
