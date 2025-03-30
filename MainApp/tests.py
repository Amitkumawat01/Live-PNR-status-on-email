# def format_pnr_status_text(response_data):
#     try:
#         # Extracting the main details
#         pnr_number = response_data.get('pnrNumber', 'N/A')
#         date_of_journey = response_data.get('dateOfJourney', 'N/A')
#         train_number = response_data.get('trainNumber', 'N/A')
#         train_name = response_data.get('trainName', 'N/A')
#         source_station = response_data.get('sourceStation', 'N/A')
#         destination_station = response_data.get('destinationStation', 'N/A')
#         reservation_upto = response_data.get('reservationUpto', 'N/A')
#         boarding_point = response_data.get('boardingPoint', 'N/A')
#         journey_class = response_data.get('journeyClass', 'N/A')
#         number_of_passengers = response_data.get('numberOfpassenger', 'N/A')
#         chart_status = response_data.get('chartStatus', 'N/A')
#         booking_fare = response_data.get('bookingFare', 'N/A')
#         quota = response_data.get('quota', 'N/A')
#         booking_date = response_data.get('bookingDate', 'N/A')
#         arrival_date = response_data.get('arrivalDate', 'N/A')
#         distance = response_data.get('distance', 'N/A')

#         # Extracting passenger details
#         passenger_details = ""
#         for passenger in response_data.get('passengerList', []):
#             passenger_details += (
#                 f"Passenger {passenger.get('passengerSerialNumber', 'N/A')}:\n"
#                 f"  Booking Status: {passenger.get('bookingStatus', 'N/A')}\n"
#                 f"  Coach: {passenger.get('bookingCoachId', 'N/A')}\n"
#                 f"  Berth: {passenger.get('bookingBerthNo', 'N/A')} ({passenger.get('bookingBerthCode', 'N/A')})\n"
#                 f"  Current Status: {passenger.get('currentStatus', 'N/A')}\n\n"
#             )

#         # Constructing the full message
#         message = (
#             f"PNR Status:\n"
#             f"PNR Number: {pnr_number}\n"
#             f"Date of Journey: {date_of_journey}\n"
#             f"Train Number: {train_number}\n"
#             f"Train Name: {train_name}\n"
#             f"From: {source_station}\n"
#             f"To: {destination_station}\n"
#             f"Reservation Upto: {reservation_upto}\n"
#             f"Boarding Point: {boarding_point}\n"
#             f"Class: {journey_class}\n"
#             f"Number of Passengers: {number_of_passengers}\n"
#             f"Chart Status: {chart_status}\n"
#             f"Booking Fare: {booking_fare} INR\n"
#             f"Quota: {quota}\n"
#             f"Booking Date: {booking_date}\n"
#             f"Arrival Date: {arrival_date}\n"
#             f"Distance: {distance} Km\n\n"
#             f"Passenger Details:\n{passenger_details}"
#         )

#         return message

#     except Exception as e:
#         return f"An error occurred while formatting the PNR status: {str(e)}"

# # Example usage
# response_data = {
#     "pnrNumber": "2658655691",
#     "dateOfJourney": "Mar 16, 2025 12:00:00 AM",
#     "trainNumber": "12963",
#     "trainName": "MEWAR EXPRESS",
#     "sourceStation": "NZM",
#     "destinationStation": "UDZ",
#     "reservationUpto": "UDZ",
#     "boardingPoint": "NZM",
#     "journeyClass": "3A",
#     "numberOfpassenger": 1,
#     "chartStatus": "Chart Not Prepared",
#     "passengerList": [
#         {
#             "passengerSerialNumber": 1,
#             "bookingStatus": "CNF",
#             "bookingCoachId": "B6",
#             "bookingBerthNo": 56,
#             "bookingBerthCode": "SU",
#             "currentStatus": "CNF"
#         }
#     ],
#     "bookingFare": 1130,
#     "quota": "GN",
#     "bookingDate": "Feb 20, 2025 12:00:00 AM",
#     "arrivalDate": "Mar 17, 2025 12:00:00 AM",
#     "distance": 743
# }

# formatted_text = format_pnr_status_text(response_data)
# print(formatted_text)


# import os
# from google.cloud import vision

# def detect_text_from_image(image_path):
#     """Detects text in an image using Google Cloud Vision API.

#     Args:
#         image_path: The path to the image file.

#     Returns:
#         The detected text as a string, or None if an error occurs.
#     """

#     try:
#         # Ensure environment variable GOOGLE_APPLICATION_CREDENTIALS is set
#         if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
#             raise Exception("Environment variable GOOGLE_APPLICATION_CREDENTIALS must be set.")

#         client = vision.ImageAnnotatorClient()

#         with open(image_path, 'rb') as image_file:
#             content = image_file.read()

#         image = vision.Image(content=content)

#         response = client.text_detection(image=image)

#         if response.error.message:
#             raise Exception(
#                 '{}\nFor more info on error messages, check: '
#                 'https://cloud.google.com/apis/design/errors'.format(
#                     response.error.message))

#         if response.text_annotations:
#             return response.text_annotations[0].description  # Extract the full text
#         else:
#             return None  # No text detected

#     except Exception as e:
#         print(f"Error detecting text: {e}")
#         return None


# # Example usage:
# image_path = "Captcha/0_p.png"  # Replace with the actual path to your image
# detected_text = detect_text_from_image(image_path)

# if detected_text:
#     print(f"Detected text:\n{detected_text}")
# else:
#     print("No text detected or an error occurred.")


import os

environment_variables = os.environ.get('DB_PASSWORD')
v = os.environ.get("OCR_SPACE_API_KEY")
print(environment_variables,v)
# Print all environment variables
# for key, value in environment_variables.items():
#     print(f"{key}={value}")

# Access a specific variable (e.g., PATH)
# path_variable = os.environ.get("PATH")
# print(f"PATH: {path_variable}")