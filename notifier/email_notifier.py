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
        self.server = None
    
    def connect(self):
        """连接SMTP服务器"""
        # 检查是否启用了邮件功能
        if not self.host or not self.user or not self.password:
            print("邮件功能未启用或配置不完整")
            return
            
        try:
            self.server = smtplib.SMTP(self.host, self.port)
            self.server.starttls()
            self.server.login(self.user, self.password)
            print("SMTP服务器连接成功")
        except Exception as e:
            print(f"连接SMTP服务器时出错: {e}")
            self.server = None
    
    def send_notification(self, report: str):
        """发送邮件通知"""
        # 检查是否启用了邮件功能
        if not self.host or not self.user or not self.password:
            print("邮件功能未启用，跳过发送通知")
            return
            
        try:
            # 检查SMTP连接
            if self.server is None:
                print("请先连接SMTP服务器")
                return
            
            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = self.user
            msg['To'] = ", ".join(self.recipients)
            msg['Subject'] = "GitHub Sentinel - 仓库更新报告"
            
            # 添加邮件内容
            msg.attach(MIMEText(report, 'plain'))
            
            # 发送邮件
            self.server.send_message(msg)
            
            print("邮件通知发送成功")
            
        except Exception as e:
            print(f"发送邮件通知时出错: {e}")
    
    def disconnect(self):
        """断开SMTP服务器连接"""
        if self.server:
            self.server.quit()
            self.server = None