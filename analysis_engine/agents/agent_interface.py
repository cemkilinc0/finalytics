app_name = "analysis_engine"

import structlog
from abc import ABC, abstractmethod
from analysis_engine.lib.promts import PromptLib

logger = structlog.get_logger()


class AgentInterface(ABC):
    def __init__(self, company_profile: dict[str, str], statements: list[dict[str, str]]):
        self.company_profile = company_profile
        self.statements = statements

    @abstractmethod
    def run(self) -> dict:
        pass

    def get_prompt(self, key: str) -> str:
        return PromptLib(self.company_profile["name"], key).get_prompt()
