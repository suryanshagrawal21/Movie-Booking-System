import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config_manager import ConfigManager

class EmailHelper:
    """Utility class to send emails via Gmail SMTP."""
    
    @staticmethod
    def send_email(to_email, subject, body):
        config = ConfigManager.load_config()
        
        # We expect these keys to be in config.json
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = config.get("email_user")
        sender_password = config.get("email_password") # User should provide App Password
        
        if not sender_email or not sender_password:
            return False, "Email credentials not found in config.json"
            
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            return True, "Email sent successfully"
        except Exception as e:
            return False, str(e)
