import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import settings


class EmailNotifier:
    def __init__(self):
        self.host = settings.EMAIL_HOST
        self.port = settings.EMAIL_PORT
        self.user = settings.EMAIL_USER
        self.password = settings.EMAIL_PASSWORD
        self.recipients = settings.EMAIL_RECIPIENTS
    
    def send_notification(self, report: str):
        """发送邮件通知"""
        try:
            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = self.user
            msg['To'] = ", ".join(self.recipients)
            msg['Subject'] = "GitHub Sentinel - 仓库更新报告"
            
            # 添加邮件内容
            msg.attach(MIMEText(report, 'plain'))
            
            # 连接SMTP服务器并发送邮件
            server = smtplib.SMTP(self.host, self.port)
            server.starttls()
            server.login(self.user, self.password)
            server.send_message(msg)
            server.quit()
            
            print("邮件通知发送成功")
            
        except Exception as e:
            print(f"发送邮件通知时出错: {e}")