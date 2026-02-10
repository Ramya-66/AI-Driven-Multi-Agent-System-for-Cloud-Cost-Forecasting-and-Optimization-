from cloud_cost_ai.services.logger import get_logger

logger = get_logger("CoordinatorAgent")

class CoordinatorAgent:
    def __init__(self, data_agent, forecast_agent, driver_agent, optimization_agent, simulation_agent):
        self.data_agent = data_agent
        self.forecast_agent = forecast_agent
        self.driver_agent = driver_agent
        self.optimization_agent = optimization_agent
        self.simulation_agent = simulation_agent

    def run_system(self):
        logger.info("Coordinator starting system run...")

        data = self.data_agent.get_data()
        forecasts = self.forecast_agent.run_forecast()
        driver_report = self.driver_agent.analyze_cost_drivers()
        recommendations = self.optimization_agent.recommend_savings()
        simulation = self.simulation_agent.simulate_what_if()

        return {
            "forecasts": forecasts,
            "driver_report": driver_report,
            "recommendations": recommendations,
            "simulation": simulation
        }
