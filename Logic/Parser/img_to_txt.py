import requests
import json
from App.DataHub import *

API_LAYER = get_config_obj().ImgToTextApiLayer

def img_to_text(image_path):

    url = "https://api.apilayer.com/image_to_text/upload"

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    headers = {
        "apikey": API_LAYER
    }
    response = requests.post(url, headers=headers, data=image_data)

    status_code = response.status_code
    
    result=json.loads(response.text)['all_text']

    print(f'\tMESSAGE FROM IMG_TO_TEXT RESULT : \n\t\t{result}')

    return result
