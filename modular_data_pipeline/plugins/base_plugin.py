import os
from abc import ABC, abstractmethod

EXPORTS_DIR = "exports/"
os.makedirs(EXPORTS_DIR, exist_ok=True)


class BasePlugin(ABC):
    @abstractmethod
    def fetch_data(self) -> dict:
        pass
