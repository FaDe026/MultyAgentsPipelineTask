import argparse

from llm.ollama_client import OllamaClient
from agents.market_analyst import MarketAnalystAgent
from agents.salary_estimator import SalaryEstimatorAgent
from agents.career_advisor import CareerAdvisorAgent
from agents.critic import CriticAgent
from pipeline import AgentPipeline
from utils.report_utils import save_json, save_markdown


def main(role):

    llm = OllamaClient()

    agents = [
        MarketAnalystAgent(llm),
        SalaryEstimatorAgent(llm),
        CareerAdvisorAgent(llm),
        CriticAgent(llm)
    ]

    pipeline = AgentPipeline(agents)

    result = pipeline.run(role)

    save_json(result)
    save_markdown(result)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=True)

    args = parser.parse_args()

    main(args.role)