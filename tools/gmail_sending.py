import smtplib
import os
import sys
import time
import env_settings as env
import pandas as pd

#please delete the password
#test no problem
# if email sending failed,please check the password and the "Allow less secure apps" setting value of the gmail account
def send_email(user, pwd, recipient_list, subject, body):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient_list if type(recipient_list) is list else [recipient_list]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        # SMTP_SSL Example
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        #server_ssl=smtplib.SMTP('smtp.gmail.com', 587)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(gmail_user, gmail_pwd)
        #time.sleep(0.5)
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
        server_ssl.sendmail(FROM, TO, message)
        #server_ssl.quit()
        server_ssl.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")


def main(user, pwd, recipient_list, subject, body):
    send_email(user, pwd, recipient_list, subject, body)

def get_gmail_info():
    pd_data=pd.read_excel()
    print("not finished.....")

    info_dict={
        "user":"",
        "pwd":""
    }
    return info_dict

def gmail_test():
    gmail_info=get_gmail_info()

    recipient_list=["hanzhong1987@gmail.com","hanzhong2018@docomo.ne.jp"]
    subject="test mail"
    body="hello"
    main(user, pwd, recipient_list, subject, body)

if __name__=="__main__":
    """
    user=os.argv[1]
    pwd=os.argv[2]
    recipient_list=os.argv[3]
    subject=os.argv[4]
    body=os.argv[5]
    main(user, pwd, recipient_list, subject, body)
    """
    gmail_test()