import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "simulated_realtime_cloud_cost.csv")
PLOT_DIR = os.path.join(BASE_DIR, "outputs", "accuracy_plots")

os.makedirs(PLOT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])

print("Dataset loaded from:", DATA_PATH)
print("Shape:", df.shape)

def time_series_split(df, ratio=0.8):
    split = int(len(df) * ratio)
    return df.iloc[:split], df.iloc[split:]

def forecast_service(service_df, periods):
    model = Prophet(daily_seasonality=True)
    model.fit(service_df)
    future = model.make_future_dataframe(periods=periods)
    return model.predict(future)

def accuracy_metrics(actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    return mae, rmse, mape

results = []
services = df["service"].unique()

for service in services:
    service_df = (
        df[df["service"] == service]
        .groupby("date")["cost_usd"]
        .sum()
        .reset_index()
        .rename(columns={"date": "ds", "cost_usd": "y"})
        .sort_values("ds")
    )

    train, test = time_series_split(service_df)

    forecast = forecast_service(train, periods=len(test))

    predicted = forecast.tail(len(test))["yhat"].values
    actual = test["y"].values
    dates = test["ds"].values

    mae, rmse, mape = accuracy_metrics(actual, predicted)

    results.append({
        "Service": service,
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "MAPE (%)": round(mape, 2)
    })

    # 📈 Actual vs Predicted Plot
    plt.figure(figsize=(10, 5))
    plt.plot(dates, actual, label="Actual Cost", marker="o")
    plt.plot(dates, predicted, label="Predicted Cost", linestyle="--")
    plt.title(f"Actual vs Predicted Cost – {service}")
    plt.xlabel("Date")
    plt.ylabel("Cost (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(os.path.join(PLOT_DIR, f"{service}_actual_vs_predicted.png"))
    plt.close()

results_df = pd.DataFrame(results)
print("\nForecast Accuracy Results:\n")
print(results_df)
