
# Main-App 
import streamlit as st
import pandas as pd
import folium
import openrouteservice
from streamlit_folium import st_folium
from State import State
from Decision import Decision
from Exogenous_Information import get_exogenous_info
from Transition_Function import transition
from Objective_Function import objective_function

# Load Data
@st.cache_data
def load_data():
    travel_data = pd.read_csv("data/uk_flexible_travel_dataset.csv")
    city_coordinates = pd.read_csv("data/uk_city_coordinates.csv")
    return travel_data, city_coordinates

travel_data, city_coordinates = load_data()

# Function to fetch city coordinates
def get_coordinates(city, coordinates_df):
    city_data = coordinates_df[coordinates_df["City"] == city]
    return city_data.iloc[0]["Latitude"], city_data.iloc[0]["Longitude"]

st.title("Travel Decision Maker")
st.sidebar.header("Input Parameters")

# User Inputs
start_city = st.sidebar.selectbox("Select Start City", travel_data["Start City"].unique())
destination_city = st.sidebar.selectbox("Select Destination City", travel_data["Destination City"].unique())
travel_mode = st.sidebar.selectbox("Travel Mode", travel_data["Travel Mode"].unique())
budget = st.sidebar.number_input("Enter your budget (GBP)", min_value=10, value=100, step=10)
time_left = st.sidebar.number_input("Enter available time (hours)", min_value=1, value=10, step=1)
accommodation_required = st.sidebar.checkbox("Accommodation Required?")

# Accommodation cost logic
acc_cost = 0.0
if accommodation_required:
    acc_cost = st.sidebar.number_input(
        "Accommodation Cost (leave blank for average)", min_value=0.0, value=0.0, step=10.0
    )
    if acc_cost == 0.0:
        avg_acc_cost = travel_data[travel_data["Destination City"] == destination_city][
            "Accomodation Average Price Per Night (GBP)"
        ].mean()
        acc_cost = avg_acc_cost

# Button to trigger calculation
if st.sidebar.button("Calculate Best Travel Decision"):
    # shows unique destinations that are not the same as start_city
    possible_destinations = travel_data[travel_data["Start City"] == destination_city]["Destination City"].unique()

    # State and Decision setup
    state = State(location=start_city, budget=budget, time_left=time_left, next_available_destinations=possible_destinations)
    decision = Decision(destination=destination_city, mode_of_travel=travel_mode, accommodation_cost=acc_cost)

    # Fetch Exogenous Information
    ex_info = get_exogenous_info()

    # Transition and Objective Evaluation
    new_state, transition_messages = transition(state, decision, ex_info, travel_data)
    score = objective_function(new_state, decision, ex_info)


    # Save results in session state
    st.session_state["new_state"] = new_state
    st.session_state["score"] = score
    st.session_state["ex_info"] = ex_info
    st.session_state["transition_messages"] = transition_messages

# Check if the calculation is done
if "new_state" in st.session_state:
    st.subheader("Results")
    st.write(f"**Updated State:**")
    st.json(vars(st.session_state["new_state"]))
    st.write(f"**Objective Function Score:** {st.session_state['score']:.2f}")

    # Display Transition Messages
    st.subheader("Process Details")
    transition_messages = st.session_state["transition_messages"]
    for message in transition_messages:
        st.write(f"- {message}")

    # Exogenous Information
    ex_info = st.session_state["ex_info"]
    st.subheader("Exogenous Factors")
    st.write(f"**Weather:** {ex_info['weather']}")
    st.write(f"**Events:** {ex_info['events']}")
    st.write(f"**Travel Deals (Discount):** {ex_info['travel_deals']['Discount']}%")
    st.write(f"**Restrictions:** {ex_info['restrictions']}")

    # Generate and Display Map
    start_lat, start_lon = get_coordinates(start_city, city_coordinates)
    dest_lat, dest_lon = get_coordinates(destination_city, city_coordinates)

    # OpenRouteService API integration for route map
    api_key = "5b3ce3597851110001cf6248f26b5f1df0244830a04e1da5519f9689"  
    client = openrouteservice.Client(key=api_key)

    # Function to generate the route map
    def generate_map():
        # Request directions from OpenRouteService
        route = client.directions(
            coordinates=[(start_lon, start_lat), (dest_lon, dest_lat)],
            profile='driving-car',  # Use driving-car profile for road routes
            format='geojson'
        )
        # Extract coordinates of the route
        route_coordinates = [(point[1], point[0]) for point in route['features'][0]['geometry']['coordinates']]

        m = folium.Map(location=[start_lat, start_lon], zoom_start=6)
        folium.Marker([start_lat, start_lon], popup=start_city, icon=folium.Icon(color="blue")).add_to(m)
        folium.Marker([dest_lat, dest_lon], popup=destination_city, icon=folium.Icon(color="red")).add_to(m)
        folium.PolyLine(route_coordinates, color="green", weight=2.5).add_to(m)

        st.subheader("Route Map")
        st_folium(m, width=700, height=500)
        
    # Display the map 
    generate_map()


else:
    st.info("Please fill in the inputs and click 'Calculate Best Travel Decision' to see the results.")


