class Beautifier:
    """
    Class that creates HTML file (_filename) with simple w3-css style from
    input dict (_data).  Example of input dict:

    { 'WI-FI keys':
        [
            {'ESSID': 'Burger-king', 'Pass': 'testtest'},
            {'ESSID': 'Neighboring Wi-Fi', 'Pass': '12345678'},
            {'ESSID': 'MyWi-Fi', 'Pass': 'pr0Sup3erH4cker!'},
        ],
      'Chrome passes':
        [
            {'URL': 'facebook.com', 'Login': 'destoyer228', 'Pass': '1234'},
            {'URL': 'github.com', 'Login': 'kovinevmv', 'Pass': 'so_secret_info'},
        ]
    }
    """

    def __init__(self, _filename, _data):
        """ Create file with _filename and write not empty data """
        self.filename = _filename
        self.data = _data

        self.html_file = open(self.filename, 'wb')

        if self.data:
            self.write_data()

    def create_head(self):
        """
        Write head of HTML.  Added w3-css to avoid external
        dependency and work without Internet.
        """
        self.html_file.write(
            '<html><style type="text/css">.w3-table{table-layout: fixed;}.w3-third{width:33.33333%}.w3-table td,'
            '.w3-table th,.w3-table-all td,.w3-table-all th{padding:8px 8px;display:table-cell;text-align:left '
            ';vertical-align:top}.w3-table th:first-child,.w3-table td:first-child,.w3-table-all th:first-child'
            ',.w3-table-all td:first-child{padding-left:16px}h1,h2,h3,h4,h5,h6{font-family:"Segoe UI",Arial,san'
            's-serif;font-weight:400;margin:10px 0}html{box-sizing:border-box}*,*:before, *:after{box-sizing:in'
            'herit}html,body{font-family:Verdana,sans-serif;font-size:15px;line-height:1.5}html{overflow-x:hidd'
            'en}.w3-teal{color:#fff!important;background-color:#009688!important}.w3-container{padding:0.01em 1'
            '6px}.w3-center{text-align:center}.w3-margin-left{margin-left:16px!important}.w3-table{border-colla'
            'pse:collapse;border-spacing:0;width:100%;display:table}.w3-table td,.w3-table th.w3-table th:first'
            '-child,.w3-table td:first-child.w3-bordered tr,.w3-table-all tr{border-bottom:1px solid #ddd}.w3-b'
            'lue{color:#fff!important;background-color:#2196F3!important}.w3-container{padding:0.01em 16px}.w3-'
            'red{color:#fff!important;background-color:#f44336!important}</style>'.encode('utf-8'))

    def write_end(self):
        """ Write end of HTML """
        self.html_file.write('</html>'.encode('utf-8'))
        self.html_file.close()

    def add_head(self, text):
        """
        Add above table bar with description of table.
        In example it's a 'WI-FI keys' or 'Chrome passes'.
        """
        self.html_file.write(('<h1 class=\"w3-teal w3-container w3-center\">' + text + '</h1>\n').encode('utf-8'))

    def add_table(self, heads):
        """ Create table.  Add heads of table. """
        tag = '<div class=\"w3-margin-left \"><table class=\"w3-table w3-bordered\">\n<tr class=\"w3-blue\">'
        for head in heads:
            tag += '<th class=\"w3-third\">' + head
        tag += '</th></tr>\n'

        self.html_file.write(tag.encode('utf-8'))

    def add_table_end(self):
        """ Write end of table """
        self.html_file.write("</table></div>".encode('utf-8'))

    def get_heads(self, index):
        """
        Get keys of subdictionaries.
        In example it's ['ESSID', 'Pass'] or ['URL', 'Login', 'Pass']
        """
        return list(list(self.data.values())[index][0].keys())

    def add_data(self, data):
        """
        Write content of each subdictionary.
        In example it's a value of 'WI-FI keys' or 'Chrome passes'.
        """
        for row in data:
            self.html_file.write('<tr>'.encode('utf-8'))
            for key, value in row.items():
                self.html_file.write(("<td class=\"w3-third\">" + value).encode('utf-8'))
            self.html_file.write('</tr>\n'.encode('utf-8'))

    def write_data(self):
        """ Write main dictionary to file.  For each sudictionaty create new table. """
        self.create_head()
        for index, (header, value) in enumerate(self.data.items()):
            if value:
                self.add_head(header)
                self.add_table(self.get_heads(index))
                self.add_data(value)
                self.add_table_end()
        self.write_end()


if __name__ == '__main__':
    pass
