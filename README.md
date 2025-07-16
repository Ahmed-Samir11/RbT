# RbT: Real-time Carbon and WeatherBench2 Model Evaluation Platform

## Overview
RbT is a platform for analyzing, predicting, and evaluating carbon emissions using both real-time UK carbon intensity data and the WeatherBench2 global weather benchmark. It features a modern React frontend and a FastAPI backend, supporting:
- **Live UK Carbon Intensity Analysis**
- **WeatherBench2 Model Evaluation** (using official cloud datasets)
- **Side-by-side Data Analysis and Visualization**

## Features
- Home page with three options: Real-time UK Carbon, WeatherBench2 Evaluation, and Compare Both
- Real-time data analysis and visualization
- Model evaluation on WeatherBench2 public datasets (cloud Zarr)
- Feedback loop and retraining support

## Quick Start

### Prerequisites
- Python 3.9+ (for backend)
- Node.js 16+ and npm (for frontend)
- (Windows) Microsoft C++ Build Tools (for some Python dependencies)

### Backend Setup
1. Install dependencies:
   ```sh
   pip install --upgrade pip setuptools wheel
   pip install -r rbt-web/requirements.txt
   pip install git+https://github.com/google-research/weatherbench2.git
   ```
2. Start the backend:
   ```sh
   uvicorn rbt-web.backend.app:app --reload
   ```

### Frontend Setup
1. In a new terminal:
   ```sh
   cd rbt-web/frontend
   npm install
   npm start
   ```
2. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Usage
- **Home Page:** Choose between Real-time UK Carbon, WeatherBench2 Evaluation, or Compare Both.
- **/realtime:** View live UK carbon intensity and grid mix analysis.
- **/weatherbench:** Evaluate the model on WeatherBench2 public datasets (no local download needed).
- **/compare:** Compare model performance and data analysis side-by-side.

## WeatherBench2 Integration
- Uses official [WeatherBench2](https://github.com/google-research/weatherbench2) Python package and public cloud Zarr datasets.
- No need to download large datasets locally; data is streamed from GCS.
- Requires `gcsfs`, `xarray`, `zarr`, and `apache-beam` (see requirements.txt).

## Notes
- For Windows users: If you see C++ build errors, ensure you have the "Desktop development with C++" workload installed via Visual Studio Installer.
- For Docker: Update your Dockerfile to include all Python dependencies if deploying in containers.

## License
Apache-2.0

