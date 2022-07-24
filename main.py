import requests
import smtplib
from datetime import datetime
import time
import os

# Constants
MY_LAT = int(os.environ.get("MY_LAT"))
MY_LONG = int(os.environ.get("MY_LONG"))

MY_EMAIL = os.environ.get("MY_EMAIL")
EMAIL_PASSWORD = os.environ.get("MY_PASSWORD")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL")

ISS_ENDPOINT = "http://api.open-notify.org/iss-now.json"
SUNSET_SUNRISE_ENDPOINT = "https://api.sunrise-sunset.org/json"

# Determine longitude and latitude of International Space Station
response = requests.get(url=ISS_ENDPOINT)
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# Determine the sunrise and sunset times at my location
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get(url=SUNSET_SUNRISE_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()

sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

# Check for ISS sighting
while True:
    time.sleep(60)
    time_now = datetime.now()
    # Is the ISS is close to current position
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        # Is it dark enough outside to be able to see ISS overhead
        if time_now.hour <= sunrise or time_now.hour >= sunset:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=EMAIL_PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL, to_addrs=RECIPIENT_EMAIL,
                                    msg="Subject:ISS Overhead!\n\nTake a look outside! The International Space Station "
                                        "is passing overhead.")
