import sys
import os
import requests
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend import database

def fetch_and_save_uk_carbon_intensity():
    # Fetch current carbon intensity
    ci_url = "https://api.carbonintensity.org.uk/intensity"
    gen_url = "https://api.carbonintensity.org.uk/generation"
    ci_resp = requests.get(ci_url)
    gen_resp = requests.get(gen_url)
    ci_resp.raise_for_status()
    gen_resp.raise_for_status()
    ci_data = ci_resp.json()['data'][0]
    gen_data = gen_resp.json()['data'][0]

    # Extract values
    timestamp = ci_data['from']
    carbon_intensity = ci_data['intensity']['actual'] or ci_data['intensity']['forecast']
    generation_mix = gen_data['generationmix']

    # Example: Save as a prediction (industry, renewables, population are placeholders)
    # You may want to map real data to your model's expected inputs
    industry = sum([g['perc'] for g in generation_mix if g['fuel'] in ['coal', 'gas', 'oil', 'other']])
    renewables = sum([g['perc'] for g in generation_mix if g['fuel'] in ['wind', 'solar', 'hydro', 'biomass']])
    population = 1_000_000  # Placeholder, as API does not provide this
    emissions = carbon_intensity  # gCO2/kWh
    sdg_score = max(0, min(100, 100 - emissions))
    pred_id = database.save_prediction([industry, renewables, population], emissions, sdg_score)
    print(f"Saved real-time UK carbon intensity: {emissions} gCO2/kWh, prediction_id: {pred_id}")

if __name__ == "__main__":
    fetch_and_save_uk_carbon_intensity()
