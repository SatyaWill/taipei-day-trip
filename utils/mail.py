from email.message import EmailMessage
from setting import MAIL, MAIL_PW, VERIFICATION_URL
import ssl, smtplib

def send_verification_email(name, receiver, token):
    em = EmailMessage()
    em["From"] = MAIL
    em["To"] = receiver
    em["Subject"] = "台北一日遊註冊驗證信"
    verification_url = VERIFICATION_URL + '?token=' + token
    content = '<p>' + name + '您好：</p><p>您申請註冊本站會員，請點擊以下連結進行驗證:</p><p><a href="'\
            + verification_url + '">' + verification_url + '</a></p>'
    em.set_content(content, subtype='html')

    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
    server.login(MAIL, MAIL_PW)
    server.sendmail(MAIL, receiver, em.as_string())
    server.close()

    


