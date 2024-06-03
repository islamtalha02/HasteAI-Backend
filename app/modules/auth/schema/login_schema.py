from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str
    user_role: str