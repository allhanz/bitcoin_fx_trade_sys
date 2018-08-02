import time
import sys
from email.mime.text import MIMEText
from email.utils import formatdate
import smtplib
#please delete the password
#test ok
#single email address sending tools
class send_email_tool:
    def __init__(self,username,passwd):
        self.username = username
        self.passwd = passwd
        self.s = smtplib.SMTP('smtp.gmail.com', 587)
        self.from_add = 'hanzhong1987@gmail.com' # the sender's email
        #self.connect_mail_server()

    def connect_mail_server(self):
        try:
            if self.s.ehlo_or_helo_if_needed():
                self.s.ehlo()
            self.s.starttls()
            self.s.ehlo()
            self.s.login(self.username, self.passwd)
            return True
        except smtplib.SMTPNotSupportedError:
            self.s.login(self.username, self.passwd)
            return False
        return True

    def send_email(self, toaddress ,message):
        if self.connect_mail_server():
            try:
                self.s.sendmail(self.from_add, toaddress, message)
                print('Send a mail to %s' % (toaddress))
            except smtplib.SMTPDataError:
                print('Can not send a mail, maybe reach the daily limition')
        else:
            print("cannot connect the gmail server...")

    def recieve_email():
        print("not finished.....")


def test_main():
    usename="hanzhong1987@gmail.com"
    password="Scroll138127"
    to_addr="hanzhong2018@docomo.ne.jp"
    #to_addr="jobhunthanz@gmail.com"
    email_obj=send_email_tool(usename,password)
    email_obj.send_email(to_addr,"hello test email")

def main():
    print("not finished....")

if __name__=="__main__":
    test_main()
    
