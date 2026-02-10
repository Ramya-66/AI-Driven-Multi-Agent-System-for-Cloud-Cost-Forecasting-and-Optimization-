# main.py

from cloud_cost_ai.agents.data_agent import DataAgent
from cloud_cost_ai.agents.forecast_agent import ForecastAgent
from cloud_cost_ai.agents.driver_agent import DriverAgent
from cloud_cost_ai.agents.optimization_agent import OptimizationAgent
from cloud_cost_ai.agents.simulation_agent import SimulationAgent
from cloud_cost_ai.agents.coordinator_agent import CoordinatorAgent
from cloud_cost_ai.agents.budget_alert_agent import BudgetAlertAgent

def main(budget_limit=5000):
    """
    Entry point for Cloud Cost AI System
    budget_limit: USD, dynamic from Streamlit or default
    """

    # 1️⃣ Load data
    data_agent = DataAgent()
    data = data_agent.get_data()

    # 2️⃣ Initialize core agents
    forecast_agent = ForecastAgent(data)
    driver_agent = DriverAgent(data)

    # 3️⃣ Run forecasting
    forecasts = forecast_agent.run_forecast()

    # 4️⃣ Optimization & simulation
    cost_driver_report = driver_agent.analyze_cost_drivers()
    optimization_agent = OptimizationAgent(forecasts, cost_driver_report)
    simulation_agent = SimulationAgent(forecasts)

    # 5️⃣ Coordinator (orchestration)
    coordinator = CoordinatorAgent(
        data_agent=data_agent,
        forecast_agent=forecast_agent,
        driver_agent=driver_agent,
        optimization_agent=optimization_agent,
        simulation_agent=simulation_agent
    )

    results = coordinator.run_system()

    # 6️⃣ Budget Alert
    total_cost = data["cost_usd"].sum()
    budget_agent = BudgetAlertAgent(budget_limit=budget_limit)
    budget_status = budget_agent.check_budget(total_cost)

    # ✅ Inject into results
    results["budget_status"] = budget_status

    # 7️⃣ Console Output
    print("\n=== 📊 Cost Driver Report ===")
    print(results["driver_report"])

    print("\n=== 💡 Optimization Recommendations ===")
    for r in results["recommendations"]:
        print("-", r)

    print("\n=== 💰 Simulation Savings ===")
    for service, saving in results["simulation"].items():
        print(f"{service}: ${saving:.2f}")

    print("\n=== 🚨 Budget Status ===")
    print(results["budget_status"])

    print("\n✅ Cloud Cost AI System Executed Successfully")

    # 8️⃣ RETURN results (IMPORTANT for Streamlit)
    return results


if __name__ == "__main__":
    main()
