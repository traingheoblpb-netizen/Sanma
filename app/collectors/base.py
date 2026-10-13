from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseCollector(ABC):
    def __init__(self, source: Dict[str, Any]):
        self.source = source

    @abstractmethod
    def collect(self) -> List[Dict[str, Any]]:
        """Return list of raw records/dicts"""
        pass
