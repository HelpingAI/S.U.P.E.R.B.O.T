import requests
import time
import os

def get_bitcoin_price():
    url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        price_usd = data["bpi"]["USD"]["rate"]
        return price_usd
    else:
        return "Error fetching Bitcoin price"

if __name__ == "__main__":
    print("Welcome to Bitcoin Price Tracker microbot!")
    
    while True:
        price = get_bitcoin_price()
        print(f"Current Bitcoin Price (USD): {price}")
        
        user_input = input("Press 'q' to quit or any other key to refresh: ")
        if user_input.lower() == "q":
            print("Exiting Bitcoin Price Tracker.")
            break
    
    print("Returning to Home")
    
