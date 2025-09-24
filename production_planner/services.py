import random

def get_demand_forecast(product_history, seasonal_trends):
    """
    Simulates a call to an LLM for demand forecasting.
    In a real application, this would involve a network request to an LLM API.
    """
    # Simulate a score based on the input data.
    # This is a very simple simulation. A real one would be more complex.
    score = random.uniform(0.5, 0.9) # Start with a base score
    
    if "high_demand" in product_history:
        score += 0.1
    
    if "winter" in seasonal_trends:
        score += 0.05

    # Ensure the score is within a reasonable range
    score = min(score, 1.0)
    
    return {
        "predicted_demand_score": round(score, 2),
        "confidence": "high",
        "seasonal_adjustment": seasonal_trends
    }