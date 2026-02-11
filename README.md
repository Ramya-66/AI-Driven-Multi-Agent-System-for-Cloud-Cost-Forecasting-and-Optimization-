# AI-Driven-Multi-Agent-System-for-Cloud-Cost-Forecasting-and-Optimization
## Introduction

Managing cloud costs has become increasingly complex due to dynamic usage patterns, multiple services, and limited visibility into billing data. Many users do not have direct access to cloud cost dashboards, making proactive cost control difficult. 

Cloud Cost AI is a multi-agent intelligent system designed to analyze cloud usage data, forecast future costs, identify major cost drivers, recommend optimization strategies, simulate savings, and monitor budgets proactively.The system is built using a modular agent-based architecture, where each agent is responsible for a specific task and coordinated by a central controller.

## Multi-Agent Systems

A multi-agent system allows complex problems to be divided into independent, intelligent components, each responsible for a specific task.

In this project:

 - Each agent performs a single well-defined role.
 - Agents collaborate to produce a complete cost intelligence pipeline.
 - The system is modular, scalable, and explainable.
 - This design mirrors real-world cloud management workflows.

## System Architecture

The proposed system is built using a multi-agent architecture in which each agent is responsible for a specific task in the cloud cost management pipeline. The Coordinator Agent acts as the central controller of the system, managing the execution order of all agents and aggregating their outputs to ensure smooth data flow and coordination. The Data Agent is responsible for loading the cloud cost dataset, performing data cleaning and preprocessing, and aggregating costs by service and date before supplying structured data to other agents. The Driver Agent analyzes the processed data to identify major cloud cost drivers by calculating total expenditure per service and highlighting services that contribute the most to overall costs. The Forecast Agent applies time-series forecasting techniques using the Prophet model to predict future cloud costs for each service and generate forecast data and visual plots. Based on both historical and forecasted costs, the Optimization Agent generates actionable cost optimization recommendations by identifying potential inefficiencies and suggesting strategies to reduce cloud spending. The Simulation Agent performs what-if analysis by simulating the impact of applying optimization strategies and estimating potential cost savings. Finally, the Budget Monitoring Logic compares the forecasted cloud costs with a user-defined budget threshold, detects possible budget overruns, and generates budget alerts, enabling proactive cloud cost control.

<p align="center">
  <img width="500" height="500" alt="Untitled-2026-02-03-2215" src="https://github.com/user-attachments/assets/95b259da-90d3-4aa7-9c12-04db12ae96cf" />
  <br>
  <em>fig.System Architecture</em>
</p>

## Creating a Entry Point (main.py)

The main.py file is the starting point of the system.
It initializes all agents and triggers the workflow.
```
from cloud_cost_ai.agents.coordinator_agent import CoordinatorAgent
def main(budget_limit=5000):
    coordinator = CoordinatorAgent(budget_limit=budget_limit)
    results = coordinator.run_system()
    return results
if __name__ == "__main__":
    main()
```
## Creating Coordinator Agent ##

The Coordinator Agent is responsible for managing the execution flow between all specialized agents.
It acts as the brain of the system, ensuring that each agent runs in the correct order and that outputs are aggregated properly. Let's see how to implement this:

```
class CoordinatorAgent:
    def __init__(self, budget_limit):
        self.budget_limit = budget_limit

    def run_system(self):
        data = DataAgent().load_data()
        drivers = DriverAgent(data).analyze()
        forecasts = ForecastAgent(data).run_forecast()
        recommendations = OptimizationAgent(forecasts).generate()
        simulation = SimulationAgent(forecasts).simulate()
        budget_status = BudgetAgent(forecasts, self.budget_limit).check()

        return {
            "driver_report": drivers,
            "forecasts": forecasts,
            "recommendations": recommendations,
            "simulation": simulation,
            "budget_status": budget_status
        }
```
## Data Agent
The Data Agent is responsible for handling the raw cloud cost dataset. Now load the dataset:
```
import pandas as pd
class DataAgent:
    def load_data(self):
        df = pd.read_csv("data/simulated_realtime_cloud_cost.csv")
        df["date"] = pd.to_datetime(df["date"])
        return df
```

## Driver Agent
The Driver Agent analyzes historical cloud costs to identify major cost drivers.
```
class DriverAgent:
    def __init__(self, data):
        self.data = data

    def analyze(self):
        return self.data.groupby("service")["cost_usd"].sum()
```
## Forecast Agent
The Forecast Agent predicts future cloud costs using the Prophet time-series forecasting model.
```
from prophet import Prophet

class ForecastAgent:
    def __init__(self, data):
        self.data = data
        self.forecasts = {}

    def run_forecast(self):
        for service in self.data["service"].unique():
            df = self.data[self.data["service"] == service]
            df = df.groupby("date")["cost_usd"].sum().reset_index()
            df.columns = ["ds", "y"]

            model = Prophet()
            model.fit(df)

            future = model.make_future_dataframe(periods=30)
            forecast = model.predict(future)

            self.forecasts[service] = forecast
        return self.forecasts
```

## Optimization Agent
The Optimization Agent analyzes both historical and forecasted cost data to generate cost-saving recommendations.
```
class OptimizationAgent:
    def __init__(self, forecasts):
        self.forecasts = forecasts

    def generate(self):
        recommendations = []
        for service, df in self.forecasts.items():
            avg_cost = df["yhat"].mean()
            if avg_cost > 100:
                recommendations.append(
                    f"Optimize {service}: high predicted usage detected"
                )
        return recommendations
```

## Simulation Agent
The Simulation Agent performs what-if cost simulations based on optimization strategies.
```
class SimulationAgent:
    def __init__(self, forecasts):
        self.forecasts = forecasts

    def simulate(self):
        savings = {}
        for service, df in self.forecasts.items():
            predicted_cost = df["yhat"].sum()
            savings[service] = predicted_cost * 0.2  # 20% savings
        return savings
```

## Budget Monitoring Logic
The Budget Monitoring module compares forecasted cloud costs against a user-defined budget limit.
```
class BudgetAgent:
    def __init__(self, forecasts, budget):
        self.forecasts = forecasts
        self.budget = budget

    def check(self):
        total_cost = sum(df["yhat"].sum() for df in self.forecasts.values())
        if total_cost > self.budget:
            return "Budget exceeded"
        return "Budget within limit"
```

## Dashboard
The Streamlit dashboard presents:

* Cost driver reports

* Forecast graphs

* Optimization recommendations

* Simulation savings

* Budget alerts

The dashboard ensures the system is easy to understand for both technical and non-technical users.

```
import streamlit as st
from main import main
results = main(budget_limit=5000)
st.title("Cloud Cost AI Dashboard")
st.dataframe(results["driver_report"])
st.success(results["budget_status"])
```

## Algorithms

- Prophet – Time-series forecasting

- Statistical aggregation – Cost analysis

- Rule-based heuristics – Optimization logic

- Simulation formulas – Savings estimation

- Threshold logic – Budget monitoring

## TechStack

- Python

- Prophet

- Pandas, NumPy

- Streamlit

- Matplotlib / Plotly

- Multi-agent modular architecture

## 👩🏻‍💼 Author 
**Ramya Srinivasan**  

