#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import requests
from urllib.parse import quote

PLD_PIN = 6
BUZZER_PIN = 20
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PLD_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Initialize the last sent time to 0
last_sent_time = 0

def send_text_message(phone_numbers, message, password):
    global last_sent_time
    current_time = time.time()
    # Check if 5 minutes (300 seconds) have passed
    if current_time - last_sent_time >= 300:
        for phone_number in phone_numbers:
            base_url = "https://theamackers.com/text/"
            encoded_message = quote(message)  # URL encode the message
            url = f"{base_url}?n=+1{phone_number}&msg={encoded_message}&password={password}"

            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print(f"Message sent successfully to {phone_number}")
                else:
                    print(f"Failed to send message to {phone_number}, status code: {response.status_code}")
            except Exception as e:
                print(f"An error occurred when sending to {phone_number}: {e}")
        last_sent_time = current_time  # Update the last sent time after all messages have been attempted
    else:
        print("Waiting to send the next message...")

phone_numbers_list = ["2069924599", "5304007823"]

while True:
    i = GPIO.input(PLD_PIN)
    if i == 0:
        print("AC Power OK")
        GPIO.output(BUZZER_PIN, 0)
    # You can remove the following comment lines (remove the # character) if you want buzzer sounds alarm.
    elif i == 1:
        print("Power Supply A/C Lost")
        send_text_message(phone_numbers_list, 'test2, multiple numbers', 'yesyoumay')
        GPIO.output(BUZZER_PIN, 1)
        time.sleep(0.1)
        GPIO.output(BUZZER_PIN, 0)
        time.sleep(0.1)
    time.sleep(1)
