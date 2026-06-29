from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """
    Base class for all document extractors.
    Every extractor must implement extract_text().
    """

    @abstractmethod
    def extract_text(self, file_path: str):
        pass