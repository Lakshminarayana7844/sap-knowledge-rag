# Forecasting basics

## Baselines
Always compare a model to simple baselines. A naive forecast repeats the last value. A seasonal naive forecast repeats the value from the same period last year.

## Backtesting
Time series backtesting trains on the past and tests on the next window, then moves the window forward. Random shuffling leaks the future into training and gives false confidence.

## Features
Useful features are lags, rolling averages, calendar fields such as week of year and holiday flags. Use only information known at forecast time.

## Metrics
MAPE is the mean absolute percentage error. It is easy to read but breaks when actual values are near zero. MAE and RMSE are alternatives.
