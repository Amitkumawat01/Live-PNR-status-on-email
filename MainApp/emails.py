import smtplib
import os

sender_email = "pnr.status.on.email@gmail.com"
app_password = "khnllerqdbxlwehp" 

def send_email(receiver_email,subject,message):
    try:
        text = f"Subject:{subject}\n\n{message}"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, text)
        
        return True,"success"
    except smtplib.SMTPException as e:
        return False,str(e)
    except Exception as e:
        return False,str(e)
    finally:
        if server:
            server.quit()  # Close the connection