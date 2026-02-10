# budget_alert_agent.py

class BudgetAlertAgent:
    def __init__(self, budget_limit):
        """
        Initialize with a dynamic budget limit.
        """
        self.budget_limit = budget_limit

    def check_budget(self, total_cost):
        """
        Compare total_cost with budget_limit.
        Returns a status string.
        """
        if total_cost > self.budget_limit:
            return f"Budget exceeded! Total cost ${total_cost:.2f} > Budget ${self.budget_limit:.2f}"
        else:
            return f"Within budget. Total cost ${total_cost:.2f} <= Budget ${self.budget_limit:.2f}"
