# IESO ML Project — Week-Ahead Zonal Load Forecasting

This repository explores interpretable, week-ahead load forecasting across IESO zones using Bayesian Ridge, Prophet, and ARIMAX, with a reusable feature engineering pipeline and rolling evaluation. The focus is on calendar structure (month/hour/weekday/holiday), persistence (1-week lag of load), Fourier seasonality, and weather/price signals.

## Project Structure
- `notebooks/`: analysis and results
  - `feature_analysis_rq2.ipynb`: feature importance (coefficients, ablation, permutation)
  - `training_testing_rq1.ipynb`: training/testing and evaluation pipelines
  - `rq3_uncertainty.ipynb`: posterior predictive uncertainty and credible intervals
- `scripts/`: data and feature engineering helpers
  - `FeatureEngineering.py`, `DemandData.py`, `WeatherData.py`, `PriceData.py`, `Centroids.py`
- `data/`: input data (see link below for large files)
  - `consolidated/`: merged weather/demand/price CSVs
  - `weather/`, `demand/`: raw per-zone inputs
- `requirements.txt`: Python dependencies
- `Dockerfile`: containerized environment

## Data Access
Large data files are hosted externally due to GitHub size limits. Download the consolidated and weather inputs from:

https://drive.google.com/drive/folders/1CzZE6E5Ik-xpq3nIN7kbFLupZ_t5OUTd?usp=share_link

Place files under `data/` following the existing structure (e.g., `data/consolidated/consolidated_weather_from_centroids.csv`).

## Quick Start (Local)
```zsh
# From the repo root
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Launch Jupyter and open notebooks in `notebooks/`
jupyter lab
```

Recommended notebook run order:
1) `training_testing_rq1.ipynb`
2) `feature_analysis_rq2.ipynb`
3) `rq3_uncertainty.ipynb`

## Docker (Optional)
```zsh
docker build -t ieso-ml .
docker run -it --rm -p 8888:8888 -v "$PWD":/workspace ieso-ml
```
Then open the Jupyter URL printed in the container.

## Methods Overview
- **Bayesian Ridge**: rolling week-ahead forecasts with expanding windows; interpretable coefficients; uncertainty via posterior predictive std and 95% credible intervals.
- **Prophet**: permutation importance for calendar regressors and key exogenous features (1w load, lagged temperature, price, precipitation).
- **ARIMAX**: linear coefficients to verify calendar/persistence dominance and cross-model consistency.

## Reproducing Key Results
- Feature importance (coefficients and ablation) and permutation importance are computed in `feature_analysis_rq2.ipynb`.
- Rolling evaluation and train/test splits are implemented in `training_testing_rq1.ipynb`.
- Uncertainty visuals and summaries are in `rq3_uncertainty.ipynb`.

## Scripts
Reusable components live under `scripts/` and are imported by the notebooks:
- `FeatureEngineering.py`: dataset cleaning, merging, calendar features, and lags
- `DemandData.py`, `WeatherData.py`, `PriceData.py`: data loaders and utilities
- `Centroids.py`: geospatial helpers for zone centroids

## Notes
- Ensure consolidated CSVs match the expected columns used by the notebooks (see `FeatureEngineering.py`).
- To save figures, create `figures/` and uncomment any `plt.savefig(...)` lines in notebooks.

