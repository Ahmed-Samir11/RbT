# RbT: A Self-Improving System for Environment and Sustainability

**Return by Train (RbT)** is a self-improving, AI-driven environmental forecasting system developed to support decision-making across critical domains such as:

- Sustainable Cities and Communities (SDG 11)
- Climate Action (SDG 13)
- Renewable Energy and Industrial Emissions
- Recycling and Waste Management
- Circular Economy Initiatives

---

## 🧠 What is RbT?

RbT leverages **Kolmogorov-Arnold Networks (KANs)** to perform high-resolution forecasting and system modeling. It integrates adaptive feedback loops and architecture evolution strategies inspired by **self-improving agents** research from Sakana AI.

Through continuous retraining and self-modification, RbT enhances its prediction accuracy and sustainability alignment over time. The system simulates environmental interactions such as industrial output, population growth, and renewable energy integration to forecast carbon emissions and their SDG impacts.

---

## 🌍 Core Features

- **KAN-Based Forecasting**: Uses `pykan` to simulate nonlinear, high-dimensional relationships between variables.
- **Self-Improving Architecture**: Dynamically adjusts model complexity (e.g., hidden layer width, neuron count, grid resolution) based on recent performance.
- **SDG Scoring Integration**: Outputs are evaluated using a simplified SDG 11.6.2 scoring metric, guiding model optimization.
- **Synthetic Data Generator**: Creates realistic environmental data and monthly updates with seasonal and stochastic variation.
- **Visualization Engine**: Automatically generates performance and architecture evolution plots for model interpretability.

---

## 📂 File Structure

```
├── ecokan_forecasting.py         # Main script: defines model, training, self-improvement
├── requirements.txt              # Dependencies (pykan, torch, matplotlib, etc.)
├── improvement_curve.png         # RMSE evolution chart
├── architecture_evolution.png    # Hidden layer change visualization
├── README.md                     # This file
```

---

## ⚙️ How It Works

### 1. **Model Definition**

The `EcoKAN` class wraps a custom `FixedKAN`, which ensures correct activation propagation through each network layer. The architecture starts with `[3, 5, 1]` representing:

- 3 input variables: Industry, Renewables, Population
- 5 hidden neurons (adjustable)
- 1 output: Carbon Emissions

### 2. **Data Generation**

```python
def generate_data(n_samples=1000):
    # Simulates emissions based on synthetic environmental factors
```

Supports both static and time-varying (monthly) data via `generate_varied_data()`.

### 3. **Training & Evaluation**

```python
self.model.fit(dataset, steps=50, lr=0.01, lamb=0.001)
```

Performance is assessed via RMSE and a normalized SDG score:

```python
rmse = sqrt(mean_squared_error(preds, y))
sdg_score = 15 - (normalized_emissions / 10)
```

### 4. **Self-Improvement Logic**

After each training cycle, the model can:

- **Prune** (reduce hidden units if performance drops)
- **Grow** (add neurons if stable)
- **Adjust Grid Resolution** (toggle between 3 and 5 grid steps)

```python
if performance_worsens:
    prune()
elif improvement_count % 2 == 0:
    grow()
elif improvement_count % 3 == 0:
    adjust_grid()
```

### 5. **Visualization & Summary**

At the end of all improvement cycles (e.g., 5 monthly updates), the system auto-generates:

- RMSE and SDG trend plots
- Architecture evolution plot
- Summary report printed to console

---

## 🔢 Sample Output

```
Cycle |  RMSE  | SDG Score | Architecture | Modification
--------------------------------------------------------
  0   |  5.43  |   11.23   |    3-5-1     | Initial
  1   |  4.87  |   11.78   |    3-6-1     | Added neuron
  2   |  4.32  |   12.25   |    3-6-1     | Adjusted grid to 3
...
```

---

## 🚀 Getting Started

### 1. Clone Repository

```bash
git clone https://github.com/your-username/RbT.git
cd RbT
```

### 2. Install Dependencies

```bash
pip install git+https://github.com/KindXiaoming/pykan.git
pip install -r requirements.txt
```

### 3. Run the Demo

```bash
python ecokan_forecasting.py
```

---

## 🌿 Future Directions

- Integration with **WeatherBench2** for real atmospheric forecasts
- Real-time data ingestion pipelines
- Graph-based or spatiotemporal KAN extensions
- Deployment as a digital twin platform

---

## 🌟 Contributions & Citations

Inspired by:

- [Sakana AI on Self-Improving Agents](https://sakana.ai)
- [Kolmogorov–Arnold Networks (KANs)](https://github.com/KindXiaoming/pykan)

Contributions welcome! Submit a PR or open an issue.

---

## 🌊 Impact Goals

RbT aims to support:

- **Egypt Vision 2030** for sustainable urbanization
- **Global SDG targets** via adaptive, data-driven environmental intelligence

