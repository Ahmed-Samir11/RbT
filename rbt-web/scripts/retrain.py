import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
import database
from model.ecokan_forecasting import EcoKAN

def retrain_model():
    # Get new data with feedback
    training_data = database.get_verified_predictions()
    if len(training_data) > 100:  # Minimum batch size
        model = EcoKAN()
        model.load_weights()
        model.fit(training_data)
        # Evaluate and save new version
        performance = model.evaluate()
        database.save_model_version(model.architecture, performance)
        # Update production model
        model.save_weights(os.path.join(os.path.dirname(__file__), '../backend/model/weights.pt'))
        print("Retraining complete. Model updated.")
    else:
        print("Not enough new data for retraining.")

if __name__ == "__main__":
    retrain_model()
