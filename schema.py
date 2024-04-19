from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserSignIn(BaseModel):
    email: str
    password: str


class BalanceUpdate(BaseModel):
    amount: int


class ExecutionTask(BaseModel):
    text: str
