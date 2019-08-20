# -*- coding: utf-8 -*-

# from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import smtplib
from my_logger import logger
import config as my_config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def SendEMail(files2mail):
    config = my_config.GetConfig()
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    sender = config['email']['sender']
    mail_user = config['email']['mail_user']  # 用户名
    mail_pass = config['email']['mail_pass']  # 口令

    receivers = []
    for recv in config['email']['receivers']:
        receivers.append(recv['qq'])

    msg = MIMEMultipart()
    msg['From'] = formataddr([u'Chant', sender])
    msg['To'] = formataddr([u'Nancy', receivers])
    msg['Subject'] = Header(config['email']['topic'], 'utf-8').encode()
    msg.attach(MIMEText(config['email']['text'], 'plain', 'utf-8'))

    for file in files2mail:
        # 添加附件
        att1 = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1.add_header(
            'Content-Disposition',
            'attachment',
            filename=Header(file, 'utf-8').encode())  # 防止中文附件名称乱码
        msg.attach(att1)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.set_debuglevel(1)
        smtpObj.sendmail(sender, receivers, msg.as_string())
        smtpObj.quit()
        logger.info("Send EMail OK")
    except smtplib.SMTPException as e:
        logger.error("Send EMail Error: " + e)


if __name__ == "__main__":
    config_file = './price_cfg.json'
    my_config.LoadConfig(config_file)
    files2mail = []
    files2mail.append("email_op.py")
    SendEMail(files2mail)
