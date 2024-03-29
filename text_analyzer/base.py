"""
This module defines abstract base classes for entities and operations within the application.

`Entity` serves as a base class for all entities with a unique identifier.
`Operation` is an abstract base class for operations, requiring subclasses to implement an `execute` method.
"""

import datetime
from abc import ABC, abstractmethod


class Entity(ABC):  # pylint: disable=R0903
    """
    A base abstract class representing an entity with a unique identifier.

    Parameters
    ----------
    entity_id : int
        Unique identifier for the entity.
    """

    def __init__(self, entity_id: int):
        self.entity_id = entity_id


class Operation(ABC):  # pylint: disable=R0903
    """
    An abstract base class for operations, requiring an execute method implementation.

    Attributes are initialized upon creation, providing a framework for derived operation classes.

    Parameters
    ----------
    operation_id : int
        Unique identifier for the operation.
    user_id : int
        Identifier of the user associated with the operation.
    operation_date : datetime.datetime
        The date and time when the operation was created or is to be executed.
    """

    def __init__(
        self, operation_id: int, user_id: int, operation_date: datetime.datetime
    ):
        self.operation_id = operation_id
        self.user_id = user_id
        self.operation_date = operation_date

    @abstractmethod
    def execute(self):
        """
        Abstract method that executes the operation.

        This method must be implemented by subclasses to define specific execution behavior.

        Raises
        ------
        NotImplementedError
            If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement the execute method.")
