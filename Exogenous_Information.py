
# Exogenous_information.py
import random

def get_exogenous_info():
    weather = random.choice(["Sunny", "Rainy", "Cloudy", "Stormy", "Foggy"])
    travel_deals = {"Discount": random.randint(0, 50)}  # Percentage discount
    events = random.choice(["Festival", "Concert", "Sports Event", "Parade", "None"])
    restrictions = random.choice(["Open", "Road Closed", "Heavy Traffic", "Construction Work", "Accident Ahead"])

    return {
        "weather": weather,
        "travel_deals": travel_deals,
        "events": events,
        "restrictions": restrictions,
    }