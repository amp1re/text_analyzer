import logging
import os
from datetime import datetime, timedelta

import bcrypt
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from database import Session
from schema import BalanceUpdate, ExecutionTask, UserRegister, UserSignIn
from text_analyzer.ml_model import MLModel
from text_analyzer.ml_service import MLService
from text_analyzer.user import User

app = FastAPI()
logging.basicConfig(level=logging.INFO)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    to_encode["sub"] = str(to_encode["sub"])
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Payload:", payload)  # Добавьте логирование payload
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials"
            )
    except JWTError as e:
        print("JWT Error:", str(e))  # Лог ошибок декодирования JWT
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user_id


@app.put("/signup")
def signup(user_input: UserRegister, db: Session = Depends(get_db)):
    user_input = user_input.dict()
    if db.query(User).filter(User.email == user_input["email"]).first() is not None:
        raise HTTPException(status_code=400, detail="Email already in use.")
    try:
        new_user = User(
            username=user_input["username"],
            email=user_input["email"],
            password=user_input["password"],
        )
        new_user.set_api_key(db)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"username": new_user.username, "email": new_user.email}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/signin")
def signin(user_input: UserSignIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_input.email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist.")
    if not bcrypt.checkpw(user_input.password.encode(), user.password.encode()):
        raise HTTPException(status_code=403, detail="Wrong credentials passed.")
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@app.put("/update_balance")
def update_balance(
    update: BalanceUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        user.update_balance(update.amount, db)
        db.commit()
        logging.info(f"Balance updated: {user.balance}")
        return {
            "message": f"{user.username} updated balance by {update.amount}, current balance = {user.balance}"
        }
    except ValueError as e:
        db.rollback()
        logging.error(f"Error updating balance: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@app.get("/execute")
def execute_task(
    task: ExecutionTask,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == current_user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    model = MLModel()
    service = MLService(model)
    task = service.execute_task(user, task.text, db)
    return task


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
