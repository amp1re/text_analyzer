import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from text_analyzer.base import Base
from text_analyzer.ml_model import MLModel
from text_analyzer.ml_service import MLService
from text_analyzer.operation_log import OperationLog
from text_analyzer.user import User

load_dotenv()

postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_user = os.getenv("POSTGRES_USER")

# Создание engine и сессии
engine = create_engine(
    f"postgresql+psycopg2://{postgres_user}:{postgres_password}@localhost:5432/text_analyzer"
)
Session = sessionmaker(bind=engine)
session = Session()

# Создание таблицы в базе данных
Base.metadata.create_all(engine)

# Создание нового пользователя и добавление его в базу данных
new_user = User(
    username="test_user", email="test@example.com", password="securepassword123"
)
new_user.set_api_key(session)
session.add(new_user)
session.commit()

# Пополнение баланса
new_user.update_balance(10, session)

# Запрос в модель
model = MLModel()
service = MLService(model)
service.execute_task(new_user, "It is so fun!", session)


# Получение пользователя из базы данных
user = session.query(User).filter_by(username="test_user").first()
if user:
    print(f"Пользователь найден: {user.username}")
else:
    print("Пользователь не найден.")

# Получение ответа на запрос из базы данных
users_request = session.query(OperationLog).filter_by(user_id=user.id).all()
df = pd.DataFrame(
    [
        {
            "ID": request.id,
            "Text": request.text,
            "Status": request.status,
            "Result": request.result,
            "Cost": request.cost_of_operation,
            "Timestamp": request.timestamp,
        }
        for request in users_request
    ]
)

print(df)

# Закрытие сессии
session.close()
