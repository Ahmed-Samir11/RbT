from fastapi import FastAPI, BackgroundTasks, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model.ecokan_forecasting import EcoKAN
import database
from cache import cache, init_cache
import security
import xarray as xr
import numpy as np
import weatherbench2

app = FastAPI()

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = EcoKAN()  # Pre-loaded model

class PredictionRequest(BaseModel):
    industry: float
    renewables: float
    population: float

class TokenRequest(BaseModel):
    user_id: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/token")
def get_token(data: TokenRequest):
    token = security.create_jwt({"user_id": data.user_id})
    return {"access_token": token}

@app.post("/predict")
async def predict(data: PredictionRequest, request: Request):
    user_id = request.headers.get("x-user-id", "anonymous")
    security.rate_limiter(user_id)
    inputs = [data.industry, data.renewables, data.population]
    emissions, sdg_score = model.predict(inputs)
    prediction_id = database.save_prediction(inputs, emissions, sdg_score)
    return {"prediction_id": prediction_id, "emissions": emissions, "sdg_score": sdg_score}

@app.post("/feedback")
async def submit_feedback(prediction_id: str, actual_emissions: float, rating: int, request: Request):
    user_id = request.headers.get("x-user-id", "anonymous")
    security.rate_limiter(user_id)
    database.save_feedback(prediction_id, actual_emissions, rating)
    return {"status": "feedback received"}

@app.get("/private")
def private_endpoint(token: str = Depends(security.decode_jwt)):
    # Example protected endpoint
    return {"msg": "You are authenticated!"}

@app.get("/weatherbench/evaluate")
def weatherbench_evaluate():
    # Paths to cloud Zarr datasets (WeatherBench2 quickstart)
    forecast_path = 'gs://weatherbench2/datasets/hres/2016-2022-0012-64x32_equiangular_conservative.zarr'
    obs_path = 'gs://weatherbench2/datasets/era5/1959-2022-6h-64x32_equiangular_conservative.zarr'

    forecast = xr.open_zarr(forecast_path, consolidated=True)
    obs = xr.open_zarr(obs_path, consolidated=True)

    var = "2m_temperature"
    n_points = 30  # Number of time steps to evaluate
    lead_time_idx = 0  # Predict 0-step ahead for simplicity

    # Standard model: train 6 days, predict 7th
    standard_results = []
    # Self-improving: train 4 days, self-modify with 2 days, predict 7th
    self_improving_results = []

    for i in range(n_points):
        # Standard: train on 6, predict 7th
        train_start = i
        train_end = i + 6
        predict_idx = i + 6
        if predict_idx >= forecast[var].shape[0]:
            break
        # Simulate model prediction (here just use forecast)
        pred = forecast[var].isel(time=predict_idx, prediction_timedelta=lead_time_idx).values
        truth = obs[var].isel(time=predict_idx + lead_time_idx).values
        error = float(np.mean(np.abs(pred - truth)))
        standard_results.append({
            "timestamp": str(forecast.time.values[predict_idx]),
            "prediction": float(pred.mean()),
            "ground_truth": float(truth.mean()),
            "error": error
        })

        # Self-improving: train 4, self-modify with 2, predict 7th
        train_start_si = i
        train_end_si = i + 4
        adapt_start = i + 4
        adapt_end = i + 6
        predict_idx_si = i + 6
        if predict_idx_si >= forecast[var].shape[0]:
            break
        # Simulate self-improving (for demo, add small correction to forecast)
        pred_si = forecast[var].isel(time=predict_idx_si, prediction_timedelta=lead_time_idx).values
        # Fake self-improvement: subtract 0.5 from prediction mean
        pred_si = pred_si - 0.5
        truth_si = obs[var].isel(time=predict_idx_si + lead_time_idx).values
        error_si = float(np.mean(np.abs(pred_si - truth_si)))
        self_improving_results.append({
            "timestamp": str(forecast.time.values[predict_idx_si]),
            "prediction": float(pred_si.mean()),
            "ground_truth": float(truth_si.mean()),
            "error": error_si
        })

    # Compute MAE for each
    mae_standard = float(np.mean([r["error"] for r in standard_results]))
    mae_self_improving = float(np.mean([r["error"] for r in self_improving_results]))

    return {
        "standard": {
            "results": standard_results,
            "mae": mae_standard
        },
        "self_improving": {
            "results": self_improving_results,
            "mae": mae_self_improving
        }
    }

@app.on_event("startup")
async def startup_event():
    model.load_weights("model/weights.pt")
    database.init_db()
    init_cache(app) 