import json
import traceback
import requests


def PALM2_PROMPT_MAKER(INPUTPROMPT):

    PALM2_PROMPT= """

        Your role in this task is crucial.
        You are here to process and transform unstructured raw trading option buying order messages
        into a structured JSON format suitable for automated order execution.
        i am going to provide you few sample input & their output so you get more clearity

        ======================== EXAMPLE 1 ========================

        INPUT:
        BUY Qty: 530 MARGIN
        CRUDEOIL 7400 CE
        Avg price: 92.47
        +*5.32L (10.85%)
        LTP: 102.50
        N

        OUTPUT:
        {
            "index": "CRUDEOIL",
            "strike_price": "7400",
            "type": "CE",
            "valid_message": true
        }

        ======================== EXAMPLE 2 ========================

        INPUT:
        Nifty
        BANKNIFTY 44900 PE
        Side
        Buy
        Product
        INTRADAY
        265.30 >
        30.2 (12.85%)

        OUTPUT:
        {
            "index": "BANKNIFTY",
            "strike_price": "44900",
            "type": "PE",
            "valid_message": true
        }

        ======================== EXAMPLE 3 ========================

        INPUT:
        POLO RIDES
        2
        UP REED BECA
        IDERS T
        B
        POLO RACE
        500
        SAGACMOTOR

        OUTPUT:
        {
            "index": "None",
            "strike_price": "None",
            "type": "None",
            "valid_message": false
        }
        
        ======================== EXAMPLE 4 ========================

        INPUT:
        FIN NIFTY 20000 PE
        Side
        Buy
        Product
        INTRADAY
        265.30 >
        30.2 (12.85%)

        OUTPUT:
        {
            "index": "FINNIFTY",
            "strike_price": "20000",
            "type": "PE",
            "valid_message": true
        }
        
        ======================== EXAMPLE 4 ========================

        INPUT:
        NIFTY 20000 PE
        13 Sep
        Side
        Buy
        Product
        INTRADAY
        265.30 >
        30.2 (12.85%)

        OUTPUT:
        {
            "index": "NIFTY",
            "strike_price": "20000",
            "type": "PE",
            "valid_message": true
        }


        INPUT: """+INPUTPROMPT+"""

        OUTPUT: """

    return PALM2_PROMPT


def text_to_info(INPUTPROMPT_INPUT):

    try:

        prompt = PALM2_PROMPT_MAKER(INPUTPROMPT_INPUT)

        YOUR_API_KEY = 'AIzaSyAT4xzbTIyuUeNfIpM6TYhCkNQ60Fu7I_M'

        url = f'https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={YOUR_API_KEY}'  # Replace YOUR_API_KEY with your actual API key

        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "prompt": {
                "text": f"{prompt}"
            },
            "temperature": 0.7,
            "top_k": 40,
            "top_p": 0.95,
            "candidate_count": 1,
            "max_output_tokens": 1024,
            "stop_sequences": [],
            "safety_settings": [
                {"category": "HARM_CATEGORY_DEROGATORY", "threshold": 1},
                {"category": "HARM_CATEGORY_TOXICITY", "threshold": 1},
                {"category": "HARM_CATEGORY_VIOLENCE", "threshold": 2},
                {"category": "HARM_CATEGORY_SEXUAL", "threshold": 2},
                {"category": "HARM_CATEGORY_MEDICAL", "threshold": 2},
                {"category": "HARM_CATEGORY_DANGEROUS", "threshold": 2}
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        print("RESPONSE FROM GOOGLE PALM API :")
        print(json.loads(response.json()['candidates'][0]['output']))
        return json.loads(response.json()['candidates'][0]['output'])
 
        
    except Exception as e:
        print("ERROR OCCURED WHILE CALLING GOOGLE PALM API")
        print(traceback.format_exc())
        return 'DEBUGING ERROR'
