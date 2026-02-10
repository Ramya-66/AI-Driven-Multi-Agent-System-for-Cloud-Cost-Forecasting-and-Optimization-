# cloud_cost_ai/agents/data_agent.py

import os
import pandas as pd
from cloud_cost_ai.services.logger import get_logger

logger = get_logger("DataAgent")

class DataAgent:
    def __init__(self, path=None):
        # Default path relative to project root
        if path is None:
            self.path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "data", "simulated_realtime_cloud_cost.csv")
            )
        else:
            self.path = path
        self.data = None

    def load_data(self):
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Data file not found at {self.path}")
        self.data = pd.read_csv(self.path, parse_dates=['date'])
        logger.info(f"Data loaded from {self.path} with shape {self.data.shape}")
        return self.data

    def get_data(self):
        return self.load_data()
