import sys
import os
import random
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend import database

def simulate_data(n=200):
    for _ in range(n):
        industry = random.uniform(10, 100)
        renewables = random.uniform(0, 100)
        population = random.uniform(1000, 1000000)
        emissions = industry * 0.5 + renewables * -0.3 + population * 0.0001 + 10
        sdg_score = max(0, min(100, 100 - emissions))
        pred_id = database.save_prediction([industry, renewables, population], emissions, sdg_score)
        # Simulate feedback for some predictions
        if random.random() < 0.7:
            actual_emissions = emissions + random.uniform(-5, 5)
            rating = random.randint(1, 5)
            database.save_feedback(pred_id, actual_emissions, rating)
    print(f"Simulated {n} predictions and feedback.")

if __name__ == "__main__":
    simulate_data()
