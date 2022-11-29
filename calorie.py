# Using Nutritionix API to get calories

import requests
from datetime import datetime
from pytz import timezone

API_KEY = "XXXXXXXXXX"
APP_ID = "XXXXXXXXXX"
URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"

user = input("What you ate: ")

header = {
      "x-app-id": APP_ID,
      "x-app-key": API_KEY,
      "x-remote-user-id": "0"
}

parameter = {"query": user}

response = requests.post(url=URL, json=parameter, headers=header)

for i in range(len(response.json()["foods"])):
    food = response.json()["foods"][i]["food_name"]
    quantity = str(response.json()["foods"][i]["serving_qty"]) + " " + str(response.json()["foods"][i]["serving_unit"])
    calories = response.json()["foods"][i]["nf_calories"]

    date = datetime.now(timezone('Asia/Calcutta'))

    today = date.strftime("%x")
    time = date.strftime("%X")
    hour = int(date.strftime("%H"))

    if 6 <= hour < 12:
        interval = "morning"
    elif 12 <= hour < 16:
        interval = "noon"
    elif 16 <= hour < 19:
        interval = "evening"
    else:
        interval = "night"

# Using Sheety API to update data on our google sheet

    sheet_inputs = {
            "sheet1": {
                "date": today,
                "time": time,
                "interval": interval,
                "food": food,
                "quantity": quantity,
                "calories": calories
            }
        }



    adding_data = requests.post(url="https://api.sheety.co/XXXXXXXXXX/XXXXXXXXXX/XXXXXXXXXX", json=sheet_inputs)
    print(adding_data.raise_for_status())

# Using Twilio API to get SMS notification (to be run on PyhtonAnywhere)

from twilio.rest import Client
account_sid = 'XXXXXXXXXX'
auth_token = 'XXXXXXXXXX'


getting_data = requests.get(url="https://api.sheety.co/XXXXXXXXXX/XXXXXXXXXX/XXXXXXXXXX")
sheet_data = getting_data.json()
print(sheet_data)

date = datetime.now(timezone('Asia/Calcutta'))
today = date.strftime("%x")

for i in sheet_data["sheet3"]:
    if i["date"] == today:
        total = i["totalCalories"]
        print(total)
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f">\n\n Your total calorie consumption for today is {total}Kcal",
            from_='XXXXXXXXXX',
            to='XXXXXXXXXX'
        )
        print(message.status)
