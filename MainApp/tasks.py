from celery import shared_task
from datetime import datetime
from .models import EmailPNRStatus
from .emails import send_email,admin_email
from MainApp.utils import get_pnr_status_internal,format_pnr_status_text

@shared_task
def send_pnr_status_on_update():
    active_records = EmailPNRStatus.objects.filter(chartstatus="Chart Not Prepared")
    for record in active_records:
        pnr = record.pnr
        email = record.email

        currentStatusDetails_curr = [getattr(record, f"currentStatusDetails{i}") for i in range(1, 6)]

        isWL = record.isWL
        chartstatus = record.chartstatus

        try_ct=5
        while(try_ct):
            response,error = get_pnr_status_internal(pnr,email)
            try_ct = try_ct-1
            if response:
                break
        
        # print(response,error)
        if not response:
            return False
        
        isUpdated = False

        if not response.get('isWL')==isWL:
            isUpdated = True

        if not response.get('chartStatus')==chartstatus:
            isUpdated = True

        i = 1
        for passenger in response.get('passengerList', []):
            # print(passenger.get('currentStatusDetails') , currentStatusDetails_curr[i-1])
            if not passenger.get('currentStatusDetails') == currentStatusDetails_curr[i-1]:
                isUpdated = True
            i = i+1

        wl_text = {'Y': "Waiting List", 'N': "Confirmed"}
        if isUpdated:
            subject = f"PNR Status: {wl_text[response.get('isWL')]} | {response.get('chartStatus')}"
            massage = format_pnr_status_text(response)
            send_email(email,subject,massage)

        return True
        

            
@shared_task
def send_pnr_status_once(pnr,email):
    try:
        try_ct=5
        while(try_ct):
            response,error = get_pnr_status_internal(pnr,email)
            try_ct = try_ct-1
            if response:
                break
        
        if response:
            subject = f"PNR status for {pnr}"
            massage = format_pnr_status_text(response)
            send_email(email,subject,massage)
        else:
            subject = "Error Occured!"
            send_email(admin_email,subject,error)
        return True
    except Exception:
        return False
    

@shared_task
def send_otp_on_email(email,otp):
    try:
        subject = "Email Verification!"
        message = f"Hi there!\n\n Here is the OTP: {otp}"
        send_email(email,subject,message)
        return True
    except Exception as e:
        # print(str(e))
        return False