from datetime import datetime
from typing import List, Union

from sqlalchemy.orm import Session
from user_log import User

from operation_log import OperationLog


class MLService:
    def __init__(self, model, session_factory):
        self.model = model
        self.session_factory = session_factory

    def execute_task(self, user: User, text: str) -> Union[List[str], str]:
        cost_of_operation = 1
        current_datetime = datetime.now()
        session = self.session_factory()

        try:
            if user.view_balance() < cost_of_operation:
                status = "Denied"
                self.log_operation(
                    session,
                    user,
                    text,
                    status,
                    None,
                    cost_of_operation,
                    current_datetime,
                )
                return "Not enough money"

            classification_results = self.model.classify_text(text)
            status = "Success"
            user.update_balance(-cost_of_operation, session=session)
            self.log_operation(
                session,
                user,
                text,
                status,
                classification_results,
                cost_of_operation,
                current_datetime,
            )

            return classification_results
        finally:
            session.close()

    def log_operation(
        self,
        session,
        user,
        text,
        status,
        classification_results,
        cost_of_operation,
        current_datetime,
    ):
        log_entry = OperationLog(
            user_id=user.id,
            text=text,
            status=status,
            result=classification_results,
            cost_of_operation=cost_of_operation,
            timestamp=current_datetime,
        )
        session.add(log_entry)
        session.commit()
