from datetime import datetime
from typing import List, Union

from sqlalchemy.orm import Session

from .operation_log import OperationLog
from .user import User


class MLService:
    def __init__(self, model):
        self.model = model

    def execute_task(self, user: User, text: str, session) -> Union[List[str], str]:
        cost_of_operation = 1
        current_datetime = datetime.now()

        try:
            if user.view_balance(session) < cost_of_operation:
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
