
# State.py
class State:
    def __init__(self, location, budget, time_left, next_available_destinations):
        self.location = location
        self.budget = budget
        self.time_left = time_left
        self.next_available_destinations = next_available_destinations