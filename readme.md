# IESO Bayesian Load Forecasting


To look at the results, training_testing.ipynb should have most of what you're looking for. The results so far are as follows:

| Model             | RMSE (MW) | % Above Best |
|-------------------|-----------|--------------|
| Prophet           | 511.08    | 0.00%        |
| ARIMAX(1,1,1)     | 824.07    | 61.8%        |
| Bayesian Ridge    | 517.75    | 1.3%         |
