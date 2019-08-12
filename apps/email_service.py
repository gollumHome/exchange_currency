# coding: utf-8
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


class EmailApi(object):

    def __init__(self, app):
        self.from_addr = app.config['MAIL_SENDER']
        self.send_password = app.config['MAIL_PASSWORD']
        self.smtp_server = app.config['SMTP_SERVER']
        self.port = app.config['SMTP_PORT']

    def _format_addr(self, address):
        name, addr = parseaddr(address)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send_mail(self, from_addr, to_addr):
        msg = self.msg_template(to_addr)
        msg['From'] = self._format_addr('系统 <%s>' % self.from_addr)
        msg['To'] = self._format_addr('用户 <%s>' % to_addr)
        msg['Subject'] = Header('换汇平台系统邮件', 'utf-8').encode()

        server = smtplib.SMTP(self.smtp_server, self.port)
        server.login(from_addr, self.send_password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()

    def msg_template(self,to_addr):
        msg = MIMEText('<html><body><h1>please click the link to verify </h1>' +
                       '<p>send by <a href="127.0.0.1:8000/api/v1/user/user_reset_password/?confirm=true&&?email='+to_addr+'">click hear</a>...</p>' +
                       '</body></html>', 'html', 'utf-8')
        return msg