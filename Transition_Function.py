# transition.py
from State import State
import streamlit as st

def transition(state, decision, exogenous_info, dataset):
    messages = []  # List to store all output messages

    matching_data = dataset[
        (dataset["Start City"] == state.location) &
        (dataset["Destination City"] == decision.destination) &
        (dataset["Travel Mode"] == decision.mode_of_travel)
    ]

    if matching_data.empty:
        message = "No matching travel data found!"
        messages.append(message)
        return state, messages

    travel_data = matching_data.iloc[0]
    travel_cost = travel_data["Base Cost (GBP)"]
    travel_time = travel_data["Travel Time (mins)"] / 60  # Convert to hours

    if exogenous_info["restrictions"] == "Road Closed":
        message = f"Cannot travel to {decision.destination} due to road closure."
        messages.append(message)
        return state, messages

    if exogenous_info["restrictions"] == "Construction Work":
        travel_time *= 1.5  # Increase time by 50%
        messages.append("Travel time increased by 50 percent due to construction work.")

    if exogenous_info["weather"] == "Foggy":
        travel_time *= 1.2  # Increase time by 20%
        messages.append("Travel time increased by 20 percent due to foggy weather.")

    discount = exogenous_info["travel_deals"]["Discount"]
    if discount > 0:
        travel_cost *= (1 - discount / 100)
        messages.append(f"Applied a discount of {discount}% to travel cost.")

    updated_budget = state.budget - travel_cost - decision.accommodation_cost
    updated_time = state.time_left - travel_time

    if updated_budget < 0 or updated_time < 0:
        message = "Decision not feasible due to budget or time constraints."
        messages.append(message)
        return state, messages

    messages.append("Transition successful!")
    return State(decision.destination, updated_budget, updated_time, state.next_available_destinations), messages
