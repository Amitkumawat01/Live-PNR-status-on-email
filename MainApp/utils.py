import requests
import cv2
import os
from django.core import exceptions
from MainApp.models import EmailPNRStatus


API_KEY = os.environ.get("OCR_SPACE_API_KEY")

session = requests.Session()

def get_pnr_status_internal(pnr,email):
    try:
        filepath = process_image()
        if not filepath:
            raise Exception("Error downloading Captcha Image.")
        filepath = 'Captcha/0_p.png'

        ocr_response = ocr_space_file(filepath)
        # print(pnr)
        
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

        data_to_save = {
            "email":email,
            "pnr":pnr,
            "isWL":response_data.get('isWL'),
            "chartstatus":response_data.get('chartStatus'),
            "currentStatusDetails1": "",
            "currentStatusDetails2": "",
            "currentStatusDetails3": "",
            "currentStatusDetails4": "",
            "currentStatusDetails5": "",
            "currentStatusDetails6": "",
        }
        i=1
        for person in response_data["passengerList"]:
            data_to_save.update({f"currentStatusDetails{i}":person["currentStatusDetails"]}) 
            i = i+1

        EmailPNRStatus.objects.update_or_create(**data_to_save)

        if response_data.get('trainNumber'):
            return response_data, None
        else:
            error_message = "Invalid OCR Captcha or PNR Number. Please Retry!"
            return None, error_message  # Return None and the error

    except Exception as e:
        return None, str(e)

def download_image(url, save_path):
    try:
        response = session.get(url, stream=True)
        response.raise_for_status()

        os.makedirs(os.path.dirname(save_path), exist_ok=True) 

        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return True
    except requests.exceptions.RequestException:
        return False

def ocr_space_file(filename, overlay=False, api_key='K89036236388957', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """
    
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.json() 

def process_image():
    try:
        image_url = "https://www.indianrail.gov.in/enquiry/captchaDraw.png?1742047503843"
        save_location = "Captcha/0.png"

        if not download_image(image_url, save_location):
            raise Exception
        image = cv2.imread(save_location, cv2.IMREAD_UNCHANGED)
        trans_mask = image[:, :, 3] == 0
        image[trans_mask] = [255, 255, 255, 255]
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        image = cv2.bitwise_not(image)
        image = cv2.resize(image, (150, 30))

        cv2.imwrite("Captcha/0_p.png",image)
        return save_location
    except Exception:
        return None


def solve_captcha(text):
    plus = 0
    dig1 = 0
    dig = 0
    
    for i in text:
        if i=='=' or i=='?':
            break
        elif i == '+' or i == '-':
            if i == '+':
                plus = 1
            dig1 = dig
            dig = 0
        elif '0'<=i and i<='9':
            dig = dig * 10 + int(i)
        else:
            continue

    if plus:
        dig1 += dig
    else:
        dig1 -= dig
    return dig1

def get_pnr_status(captcha, pnr_number):

    try:
        base_url = f"https://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha={captcha}&inputPnrNo={pnr_number}&inputPage=PNR&language=en"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Referer": "https://www.indianrail.gov.in/enquiry/PNR/PnrEnquiry.html" # Add Referer
        }

        response = session.get(base_url, headers=headers)
        return response
    except Exception as e:
        return str(e)
    finally:
        session.close()

def format_pnr_status_text(response_data):
    try:
        # Extracting the main details
        pnr_number = response_data.get('pnrNumber', 'N/A')
        date_of_journey = response_data.get('dateOfJourney', 'N/A')
        train_number = response_data.get('trainNumber', 'N/A')
        train_name = response_data.get('trainName', 'N/A')
        source_station = response_data.get('sourceStation', 'N/A')
        destination_station = response_data.get('destinationStation', 'N/A')
        reservation_upto = response_data.get('reservationUpto', 'N/A')
        boarding_point = response_data.get('boardingPoint', 'N/A')
        journey_class = response_data.get('journeyClass', 'N/A')
        number_of_passengers = response_data.get('numberOfpassenger', 'N/A')
        chart_status = response_data.get('chartStatus', 'N/A')
        booking_fare = response_data.get('bookingFare', 'N/A')
        quota = response_data.get('quota', 'N/A')
        booking_date = response_data.get('bookingDate', 'N/A')
        arrival_date = response_data.get('arrivalDate', 'N/A')
        distance = response_data.get('distance', 'N/A')

        # Extracting passenger details
        passenger_details = ""
        for passenger in response_data.get('passengerList', []):
            passenger_details += (
                f"Passenger {passenger.get('passengerSerialNumber', 'N/A')}:\n"
                f"  Booking Status: {passenger.get('bookingStatus', 'N/A')}\n"
                f"  Coach: {passenger.get('bookingCoachId', 'N/A')}\n"
                f"  Berth: {passenger.get('bookingBerthNo', 'N/A')} ({passenger.get('bookingBerthCode', 'N/A')})\n"
                f"  Current Status: {passenger.get('currentStatus', 'N/A')}\n\n"
            )

        # Constructing the full message
        message = (
            "Hi there!\n"
            f"PNR Status:\n"
            f"PNR Number: {pnr_number}\n"
            f"Date of Journey: {date_of_journey}\n"
            f"Train Number: {train_number}\n"
            f"Train Name: {train_name}\n"
            f"From: {source_station}\n"
            f"To: {destination_station}\n"
            f"Reservation Upto: {reservation_upto}\n"
            f"Boarding Point: {boarding_point}\n"
            f"Class: {journey_class}\n"
            f"Number of Passengers: {number_of_passengers}\n"
            f"Chart Status: {chart_status}\n"
            f"Booking Fare: {booking_fare} INR\n"
            f"Quota: {quota}\n"
            f"Booking Date: {booking_date}\n"
            f"Arrival Date: {arrival_date}\n"
            f"Distance: {distance} Km\n\n"
            f"Passenger Details:\n{passenger_details}"
        )

        return message

    except Exception as e:
        return f"An error occurred while formatting the PNR status: {str(e)}"