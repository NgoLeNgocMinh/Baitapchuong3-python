import schedule
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
import shutil


sender_email = "minh_2151220169@dau.edu.vn"
sender_password = "olwr noaf wpky ewem"
receiver_email = "minh_2151220169@dau.edu.vn"

DATABASE_FOLDER = r'E:\Users\TechCare\NgoLeNgocMinh\database'
BACKUP_FOLDER = r'E:\Users\TechCare\NgoLeNgocMinh\backup'

def send_email(subject, body, recipient):
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject

  
    msg.attach(MIMEText(body, 'plain'))

    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        print(f"Email đã được gửi vào lúc {datetime.now()}")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")
    finally:
        server.quit()

def backup_database():
    try:
        files = [f for f in os.listdir(DATABASE_FOLDER) if f.endswith(('.sql', '.sqlite3'))]
        if not files:
            send_email("Backup Database", "Không có file để backup.", receiver_email)
            return
        
        for f in files:
            backup_file = os.path.join(BACKUP_FOLDER, f"{datetime.now():%Y%m%d_%H%M%S}_{f}")
            shutil.copy2(os.path.join(DATABASE_FOLDER, f), backup_file)
        
        send_email("Backup đã Thành Công", f"Đã backup {len(files)} file lúc {datetime.now():%Y-%m-%d %H:%M:%S}.", receiver_email)
    except Exception as e:
        send_email("Backup đã Thất Bại", str(e), receiver_email)


schedule.every().day.at("23:15").do(backup_database)  
schedule.every().day.at("16:00").do(backup_database)  

while True:
    schedule.run_pending()
    time.sleep(10)  
