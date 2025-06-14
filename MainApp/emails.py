import smtplib
import os

sender_email = "pnr.status.on.email@gmail.com"
app_password = os.environ.get("APP_PASSWORD")

admin_email = "amitkumarsk588@gmail.com"

def send_email(receiver_email,subject,message):
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


{'pnrNumber': '8434034135', 'dateOfJourney': 'Jun 15, 2025 5:24:00 PM', 'trainNumber': '12936', 'trainName': 'ST BDTS SF EXP', 'sourceStation': 'BL', 'destinationStation': 'VAPI', 'reservationUpto': 'VAPI', 'boardingPoint': 'BL', 'journeyClass': '2S', 'numberOfpassenger': 1, 'chartStatus': 'Chart Not Prepared', 'informationMessage': [''], 'passengerList': [{'passengerSerialNumber': 1, 'concessionOpted': False, 'forGoConcessionOpted': False, 'passengerIcardFlag': False, 'childBerthFlag': False, 'passengerNationality': 'IN', 'passengerQuota': 'RL', 'passengerCoachPosition': 0, 'waitListType': 0, 'bookingStatusIndex': 0, 'bookingStatus': 'RLWL', 'bookingBerthNo': 23, 'bookingStatusDetails': 'RLWL/23', 'currentStatusIndex': 0, 'currentStatus': 'RLWL', 'currentCoachId': '', 'currentBerthNo': 18, 'currentStatusDetails': 'RLWL/18'}], 'serverId': '', 'timeStamp': 'Jun 14, 2025 11:06:03 PM', 'bookingFare': 60, 'ticketFare': 60, 'quota': 'GN', 'reasonType': 'S', 'ticketTypeInPrs': 'E', 'vikalpStatus': 'Yes', 'waitListType': 0, 'bookingDate': 'Jun 8, 2025 12:20:37 PM', 'arrivalDate': 'Jun 15, 2025 5:43:00 PM', 'distance': 25, 'isWL': 'N', 'generatedTimeStamp': {'year': 2025, 'month': 6, 'day': 14, 'hour': 23, 'minute': 6, 'second': 3}}