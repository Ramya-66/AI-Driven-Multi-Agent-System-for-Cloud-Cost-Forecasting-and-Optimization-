from prophet import Prophet
import matplotlib.pyplot as plt

class CostForecastModel:
    def __init__(self):
        self.model = None

    def train(self, df):
        self.model = Prophet(
            daily_seasonality=True,
            yearly_seasonality=True
        )
        self.model.fit(df)
        return self.model

    def predict(self, periods=30):
        future = self.model.make_future_dataframe(periods=periods)
        forecast = self.model.predict(future)
        return forecast

    def plot_forecast(self, forecast, service_name):
        """
        Saves forecast plot for a given service
        """
        fig = self.model.plot(forecast)
        plt.title(f"Cost Forecast for {service_name}")
        plt.xlabel("Date")
        plt.ylabel("Cost (USD)")
        plt.tight_layout()
        plt.savefig(f"outputs/plots/{service_name}_forecast.png")
        plt.close()
