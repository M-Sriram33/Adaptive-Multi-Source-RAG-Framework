from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseSource(ABC):
    """
    Base interface for all data sources.

    Every source in the system such as:
    - PDF/Documents
    - SQL databases
    - APIs

    should follow this common interface.
    """

    @abstractmethod
    def can_handle(self, query: str) -> bool:
        """
        Determine whether this source can handle the query.
        """
        pass

    @abstractmethod
    def retrieve(self, query: str) -> Any:
        """
        Retrieve information relevant to the query.
        """
        pass

    @abstractmethod
    def get_source_type(self) -> str:
        """
        Return the type of source.
        Example:
        'document'
        'sql'
        'api'
        """
        pass