import smtplib

sender_email = "pnr.status.on.email@gmail.com"

admin_email = "amitkumarsk588@gmail.com"

def send_email(receiver_email,subject,message,app_password):
    try:
        text = f"Subject:{subject}\n\n{message}"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, text)
        return True
    except Exception as e:
        raise Exception(str(e))
    finally:
        if server:
            server.quit()  # Close the connection
