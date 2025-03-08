
# objective_function.py
def objective_function(state, decision, exogenous_info):
    spontaneity_score = 0

    if exogenous_info["events"] != "None":
        spontaneity_score += 10  # Bonus for attending events

    if exogenous_info["travel_deals"]["Discount"] > 0:
        spontaneity_score += 5  # Bonus for availing deals

    feasibility_penalty = max(0, -state.budget) + max(0, -state.time_left)

    # Additional penalties or bonuses based on exogenous factors
    if exogenous_info["weather"] == "Stormy":
        feasibility_penalty += 10

    if exogenous_info["restrictions"] == "Heavy Traffic":
        feasibility_penalty += 5

    total_score = spontaneity_score - feasibility_penalty
    return total_score