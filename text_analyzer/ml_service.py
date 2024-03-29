"""
This module provides the MLService class, which serves as an interface for users to execute
machine learning tasks. It manages the interaction between the user and the MLModel,
handles balance checks and deductions, and logs operations.
"""

from datetime import datetime
from typing import List, Union

from .ml_model import MLModel
from .user import User
from .utils import Sentiment


class MLService:
    """
    The MLService class encapsulates the logic required to execute machine learning
    classification tasks. It integrates user management (e.g., balance checks) with
    the execution of ML models and logs operations.

    Attributes
    ----------
    model : MLModel
        The machine learning model used for text classification tasks.

    Methods
    -------
    execute_task(user: User, text: str) -> Union[List[Sentiment], str]:
        Executes a classification task for the given text, deducts the operation cost from
        the user's balance, and logs the operation. Returns the classification results or
        an error message.
    log_operation(user, text, status, classification_results, cost_of_operation, current_datetime):
        Logs the details of an operation to a database or other persistent storage.
    """

    def __init__(self, model: MLModel):
        self.model = model

    def execute_task(self, user: User, text: str) -> Union[List[Sentiment], str]:
        """
        Executes a text classification task, deducts the operation cost, and logs the operation.

        Parameters
        ----------
        user : User
            The user who requested the task.
        text : str
            The text to classify.

        Returns
        -------
        Union[List[Sentiment], str]
            A list of Sentiment objects with classification results if successful, otherwise a string message.
        """
        cost_of_operation = 1
        current_datetime = datetime.now()
        if user.balance < cost_of_operation:
            status = "Denied"
            self.log_operation(
                user, text, status, None, cost_of_operation, current_datetime
            )
            return "Not enough money"

        classification_results = self.model.classify_text(text)
        status = "Success"
        user.update_balance(-cost_of_operation)
        self.log_operation(
            user,
            text,
            status,
            classification_results,
            cost_of_operation,
            current_datetime,
        )

        return classification_results

    def log_operation(
        self,
        user,
        text,
        status,
        classification_results,
        cost_of_operation,
        current_datetime,
    ):
        """Здесь нужна логика записи в бд"""
