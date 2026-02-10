from cloud_cost_ai.services.logger import get_logger

logger = get_logger("SimulationAgent")

class SimulationAgent:
    def __init__(self, forecasts):
        """
        forecasts: dict { service_name : forecast_dataframe }
        """
        self.forecasts = forecasts

    def simulate_what_if(self, reduction_percent=20):
        """
        Simulate savings if forecasted cost is reduced
        """
        savings_report = {}

        for service, df in self.forecasts.items():
            # ✅ FIX: use 'forecast' column, not 'yhat'
            total_predicted = df['forecast'].sum()
            potential_savings = total_predicted * reduction_percent / 100

            savings_report[service] = round(potential_savings, 2)

        logger.info("Simulation completed successfully")
        return savings_report
