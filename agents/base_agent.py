from abc import ABC, abstractmethod


class Agent(ABC):

    def __init__(self, llm_client):
        self.llm = llm_client

    @abstractmethod
    def run(self, data):
        pass