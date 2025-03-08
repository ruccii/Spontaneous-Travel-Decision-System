import pandas as pd
import random
from itertools import permutations

# Define cities and their real latitude and longitude
city_coordinates = {
    "London": (51.5074, -0.1278),
    "Birmingham": (52.4862, -1.8904),
    "Liverpool": (53.4084, -2.9916),
    "Edinburgh": (55.9533, -3.1883),
    "Bristol": (51.4545, -2.5879),
    "Cardiff": (51.4816, -3.1791),
    "Glasgow": (55.8642, -4.2518),
    "Leeds": (53.8008, -1.5491),
    "Newcastle": (54.9783, -1.6174),
    "Sheffield": (53.3811, -1.4701),
    "Nottingham": (52.9548, -1.1581),
    "Manchester": (53.4808, -2.2426),
}

# Average accommodation costs per city (in GBP)
accommodation_rates = {
    "London": 286,
    "Birmingham": 158,
    "Liverpool": 158,
    "Edinburgh": 158,
    "Bristol": 158,
    "Cardiff": 138,
    "Glasgow": 138,
    "Leeds": 138,
    "Newcastle": 138,
    "Sheffield": 138,
    "Nottingham": 138,
    "Manchester": 158
}

travel_modes = {"Car": 0.2, "Train": 0.15, "Bus": 0.1}  # Cost per km for each mode

# Generate all unique city pairs
cities = list(city_coordinates.keys())
city_pairs = list(permutations(cities, 2))

# Limit dataset size
max_rows = 2000
city_pairs = random.sample(city_pairs, min(len(city_pairs), max_rows))

# Generate dataset
data = []
for start, dest in city_pairs:
    for mode, cost_per_km in travel_modes.items():
        distance = random.randint(50, 500)  # Random distance in km
        travel_time = random.randint(30, 300)  # Random travel time in minutes
        base_cost = distance * cost_per_km
        accomodation = accommodation_rates[dest]
        start_lat, start_lon = city_coordinates[start]
        dest_lat, dest_lon = city_coordinates[dest]
        
        # Append data
        data.append([
            start, dest, mode, distance, travel_time, 
            base_cost, accomodation
        ])

# Define columns
columns = [
    "Start City", "Destination City", "Travel Mode", "Distance (km)", 
    "Travel Time (mins)", "Base Cost (GBP)", 
    "Accomodation Average Price Per Night (GBP)"
]

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Save dataset
travel_dataset_path = "data/uk_flexible_travel_dataset2.csv"
df.to_csv(travel_dataset_path, index=False)

# Create city coordinates dataset
city_coords = pd.DataFrame(
    [{"City": city, "Latitude": coords[0], "Longitude": coords[1]} for city, coords in city_coordinates.items()]
)
city_coords_path = "data/uk_city_coordinates2.csv"
city_coords.to_csv(city_coords_path, index=False)

# File paths
travel_dataset_path, city_coords_path
