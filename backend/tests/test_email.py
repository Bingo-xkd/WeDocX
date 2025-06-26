from app.services.email_service import EmailConfig, EmailService

config = EmailConfig(
    smtp_server="smtp.qq.com",
    smtp_port=465,  # 推荐用465
    smtp_user="1044553197@qq.com",
    smtp_password="viaieoturluwbeci",
    sender_email="1044553197@qq.com",
)

email_service = EmailService(config)
email_service.send_email(
    to_email="18582088138@163.com", subject="测试邮件", body="这是一封测试邮件"
)
