from cloud_cost_ai.services.logger import get_logger

logger = get_logger("OptimizationAgent")


class OptimizationAgent:
    def __init__(self, forecast, cost_driver_report):
        self.forecast = forecast
        self.cost_driver_report = cost_driver_report
        self._recommendations = None  # cache

    def recommend_savings(self, top_n=3):
        """
        Generate cost optimization recommendations
        based on top cost-driving services.
        """
        if self._recommendations is not None:
            return self._recommendations

        recommendations = set()

        # cost_driver_report is a DataFrame
        top_services = (
            self.cost_driver_report
            .groupby("service")["cost_usd"]
            .sum()
            .sort_values(ascending=False)
            .head(top_n)
            .index
            .tolist()
        )

        for service in top_services:
            if service == "EC2":
                recommendations.add(
                    "EC2 optimization: use Reserved/Spot Instances and right-size instance types."
                )
            elif service == "RDS":
                recommendations.add(
                    "RDS optimization: enable storage autoscaling and Reserved Instances."
                )
            elif service == "S3":
                recommendations.add(
                    "S3 optimization: apply lifecycle policies and move cold data to Glacier."
                )
            elif service == "Lambda":
                recommendations.add(
                    "Lambda optimization: reduce memory over-allocation and execution duration."
                )
            elif service == "DataTransfer":
                recommendations.add(
                    "Data transfer optimization: use regional endpoints and reduce cross-region traffic."
                )
            else:
                recommendations.add(
                    f"{service} optimization: review usage and apply cost controls."
                )

        logger.info("Optimization recommendations generated")
        self._recommendations = list(recommendations)
        return self._recommendations
