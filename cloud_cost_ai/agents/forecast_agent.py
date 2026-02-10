import pandas as pd
from prophet import Prophet
import logging
import os
import matplotlib.pyplot as plt

# Logger setup
logger = logging.getLogger("ForecastAgent")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class ForecastAgent:
    def __init__(self, data):
        """
        data: pandas DataFrame with columns ['date', 'service', 'region', 'cost_usd']
        """
        self.data = data.copy()
        self.forecasts = {}

    def run_forecast(self):
        """
        Generate forecasts for each service AND save plots
        """
        services = self.data['service'].unique()
        logger.info(f"Starting forecasting for services: {services}")

        for service in services:
            df_service = (
                self.data[self.data['service'] == service]
                .groupby('date')['cost_usd']
                .sum()
                .reset_index()
            )

            df_service = df_service.rename(
                columns={'date': 'ds', 'cost_usd': 'y'}
            )

            model = Prophet(daily_seasonality=True)
            model.fit(df_service)

            future = model.make_future_dataframe(periods=30)
            forecast = model.predict(future)

            forecast_df = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].rename(
                columns={
                    'ds': 'date',
                    'yhat': 'forecast',
                    'yhat_lower': 'lower',
                    'yhat_upper': 'upper'
                }
            )

            self.forecasts[service] = forecast_df

            # ✅ SAVE PLOT
            self._save_plot(service, forecast_df)

            logger.info(f"Forecast + plot completed for {service}")

        return self.forecasts

    def _save_plot(self, service, forecast_df):
        os.makedirs("outputs/plots", exist_ok=True)

        plt.figure(figsize=(10, 5))
        plt.plot(forecast_df['date'], forecast_df['forecast'], label="Forecast")
        plt.fill_between(
            forecast_df['date'],
            forecast_df['lower'],
            forecast_df['upper'],
            alpha=0.3
        )
        plt.title(f"{service} Cost Forecast")
        plt.xlabel("Date")
        plt.ylabel("Cost (USD)")
        plt.legend()
        plt.tight_layout()

        path = f"outputs/plots/{service}_forecast.png"
        plt.savefig(path)
        plt.close()

        logger.info(f"Saved plot: {path}")
