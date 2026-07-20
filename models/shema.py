from pydantic import BaseModel,Field

class TaskShema(BaseModel):
    id: int
    task: str
    status: bool | None = None

class CreateTaskShema(BaseModel):
    task: str

class User(BaseModel):
    id: int
    name: str = Field(max_length=30,description='name')
    password: str

class CreateUser(BaseModel):
    name: str = Field(max_length=30,description='name')
    password: str

class LoginUserShema(BaseModel):
    name: str = Field(max_length=30, description='name')
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInDB(User):
    hashed_password: str
