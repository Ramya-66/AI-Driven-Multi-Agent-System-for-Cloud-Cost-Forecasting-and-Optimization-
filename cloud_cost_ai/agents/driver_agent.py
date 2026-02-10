from cloud_cost_ai.services.logger import get_logger

logger = get_logger("DriverAgent")


class DriverAgent:
    def __init__(self, data):
        self.data = data
        self._driver_report = None  # cache result

    def analyze_cost_drivers(self, top_n=10):
        """
        Analyze and return top cost drivers by service and region.
        Cached to prevent duplicate computation.
        """
        if self._driver_report is not None:
            return self._driver_report

        report = (
            self.data
            .groupby(["service", "region"], as_index=False)["cost_usd"]
            .sum()
            .sort_values(by="cost_usd", ascending=False)
            .head(top_n)
        )

        logger.info("Cost driver analysis completed")
        self._driver_report = report
        return report
