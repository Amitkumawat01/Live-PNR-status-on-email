from django.shortcuts import render,redirect
from django.views import View
from django.urls import reverse
from urllib.parse import urlencode

from .models import EmailPNRStatus
from .utils import get_pnr_status,process_image,ocr_space_file,solve_captcha
from .tasks import send_pnr_status_once,send_otp_on_email

import random
from PNRStatusTracker.settings import OCR_SPACE_API_KEY,APP_PASSWORD

# Create your views here.
class PNRFormView(View):
    def get(self, request):
        return render(request, 'pnr_form.html')

    def post(self, request):
        pnr = request.POST.get('pnr')
        if pnr and pnr.isdigit() and len(pnr) == 10:  # Basic validation
            url = reverse('status')
            query_params = urlencode({"pnr": pnr})  # Encode the query parameters
            return redirect(f"{url}?{query_params}")
        else:
            return render(request, 'pnr_form.html', {'error': 'Invalid PNR number'}) # Handle invalid input


class StatusView(View):
    def get(self,request):
        try:
            pnr = request.GET.get('pnr')
            request.session['pnr']= pnr

            try_ct=5
            for i in range(try_ct):
                filepath = process_image()

                ocr_response = ocr_space_file(filepath,api_key=OCR_SPACE_API_KEY)
                
                # Check for errors in the API response
                if ocr_response.get("OCRExitCode") != 1:
                    raise Exception(ocr_response.get('ErrorMessage', 'Unknown error'))
                elif not ocr_response.get("ParsedResults"):
                    raise Exception ("No parsed results found in the OCR response.")
                else:
                    captcha_text = ocr_response["ParsedResults"][0]["ParsedText"]
                
                # print(f"Extracted Text: {captcha_text}")
                captcha_sol = solve_captcha(captcha_text)
                # print(captcha_sol)
                response = get_pnr_status(captcha_sol,pnr)
                # print(response.json())
                # print(response.status_code)
                response_data = response.json()

                if response_data.get('trainNumber'):
                    return render(request, 'pnr_status.html', {'response': response_data})
                
            error_message = response_data.get('errorMessage','Captcha not matched')
            return render(request, 'pnr_status.html', {'response': error_message}) # Pass error to template

        except Exception as e:
            return render(request, 'pnr_status.html', {'response': f"Exception occurred: {str(e)}"})

    def post(self,request):
        if request.POST.get('email'):
            email = request.POST.get('email')
            request.session['email']= email   
        else:
            email = request.session.get('email')

        pnr = request.session.get('pnr')

        otp = random.randint(1000, 9999)
        request.session['otp'] = otp

        result = send_otp_on_email.apply_async(args=[email,otp])
        # print(result)

        url = reverse('update')
        query_params = urlencode({"pnr": pnr,"email":email})  # Encode the query parameters
        return redirect(f"{url}?{query_params}")


class EmailUpdatesView(View):
    def get(self,request):
        email = request.GET.get('email')
        request.session['email']= email
        return render(request,'email_update.html',{'email':email})
    
    def post(self,request):
        pnr = request.session.get('pnr')
        email = request.session.get('email')

        filled_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')  # Retrieve from session
        
        if stored_otp is not None and int(filled_otp) == stored_otp:
            del request.session['otp']
            del request.session['pnr']
            del request.session['email']

            result = send_pnr_status_once.apply_async(args=[pnr,email,APP_PASSWORD])
            # print(result)
            return render(request,'email_update.html',{'success':"All set! You will recieve PNR updates on your Email."})
        else:
            return render(request,'email_update.html',{'failure':"Invalid otp!"}) 