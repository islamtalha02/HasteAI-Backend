from pydantic import BaseModel, EmailStr, constr

class UserRegistration(BaseModel):
    username: str
    email: str
    password: str