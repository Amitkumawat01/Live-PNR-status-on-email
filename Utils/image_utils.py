import os
import requests

def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # file_extension = os.path.splitext(url.split("/")[-1])[1]
        file_extension = ".png"
        save_path += file_extension
        os.makedirs(os.path.dirname(save_path), exist_ok=True) 

        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Image downloaded successfully: {save_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return False

if __name__ == "__main__":

    for i in range(1):
        image_url = "https://www.indianrail.gov.in/enquiry/captchaDraw.png"
        save_location = f"test_image/{i}"
        download_image(image_url, save_location)
