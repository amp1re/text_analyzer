"""
This module defines abstract base classes for entities and operations within the application.

`Entity` serves as a base class for all entities with a unique identifier.
"""

from abc import ABC


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
