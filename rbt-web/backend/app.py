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

    # Open datasets (requires gcsfs, zarr, xarray)
    forecast = xr.open_zarr(forecast_path, consolidated=True)
    obs = xr.open_zarr(obs_path, consolidated=True)

    # Example: select a variable, time, and lead_time for demo
    var = "t2m"
    time_idx = 0
    lead_time_idx = 0

    pred = forecast[var].isel(time=time_idx, prediction_timedelta=lead_time_idx).values
    truth = obs[var].isel(time=time_idx + lead_time_idx).values

    # Compute error metric (e.g., MAE)
    mae = float(np.mean(np.abs(pred - truth)))

    # Return a small sample for the frontend
    return {
        "results": [
            {
                "timestamp": str(forecast.time.values[time_idx]),
                "prediction": float(pred.mean()),
                "ground_truth": float(truth.mean())
            }
        ],
        "mae": mae
    }

@app.on_event("startup")
async def startup_event():
    model.load_weights("model/weights.pt")
    database.init_db()
    init_cache(app) 