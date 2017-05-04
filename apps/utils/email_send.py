# _*_ encoding:utf-8  _*_
from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from gycrm.settings import EMAIL_FROM


#生成随即函数
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str


def send_register_email(email,send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type=="update_email":
        code = random_str(4)
    else:
        code =  random_str(16)
    #生成一个16位长的字符
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    #发送邮件
    email_title = ""
    email_li = ""
    if send_type == "register":
        email_title = "光耀CRM系统激活连接"
        email_li = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)

        send_status=send_mail(email_title,email_li,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "光耀CRM系统密码重置链接"
        email_li = "请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_li, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "update_email":
        email_title = "光耀CRM系统邮箱修改验证码"
        email_li = "你的验证码为：{0}".format(code)
        send_status = send_mail(email_title, email_li, EMAIL_FROM, [email])
        if send_status:
            pass










