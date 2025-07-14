# RbT Web Platform

This project implements a scalable, self-improving carbon emissions forecasting and sustainability dashboard, following the provided architecture guideline.

## Structure

```
rbt-web/
├── backend/
│   ├── app.py
│   ├── model/
│   │   ├── ecokan_forecasting.py
│   │   └── weights.pt
│   ├── database.py
│   ├── cache.py
│   └── security.py
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── services/
│       ├── App.js
│       └── index.js
├── scripts/
│   ├── retrain.py
│   └── data_simulator.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Main Features
- FastAPI backend for predictions, feedback, and retraining
- PostgreSQL for data storage
- Redis for caching
- React frontend with SDG visualizations and gamified feedback
- Automated retraining and deployment pipeline

---

See each subdirectory for more details. 