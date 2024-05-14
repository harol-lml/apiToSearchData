from typing import Union
from fastapi import FastAPI
from get_data import get_data
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os
import datetime
import jwt

app = FastAPI()

load_dotenv()

# Configuración de la clave secreta
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelo para el token
class Token(BaseModel):
    access_token: str
    token_type: str

# Modelo para los datos del token
class TokenData(BaseModel):
    username: Optional[str] = None

# Modelo para el usuario
class User(BaseModel):
    username: str

# Falso almacén de datos de usuario
fake_users_db = {
    os.getenv('USER_API'): {
        "username": os.getenv('USER_API'),
        "password": os.getenv('PASSWORD_API')
    }
}

def authenticate_user(fake_db, username: str, password: str):
    user = fake_db.get(username)

    if user is None:
        return False
    if user['password'] != password:
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = fake_users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.get("/datascr")
async def read_item(id: Union[str, None] = None, per: Union[str, None] = None, pages: Union[str, None] = 1,current_user: User = Depends(get_current_user)):
    if id and per:
        data = get_data.getById(id, per, 1)
        if 'error' in data : return data
        if int(pages) <= 1: return data
        for index, number in enumerate(range(2, int(pages)), start=2):
            print(f'Número {index}: {number}')
            dt = get_data.getById(id, per, number)
            if len(dt) == 0:
                break
            data.extend(dt)
        return data
    return 'No data'

@app.get("/datam")
async def read_data(id: Union[str, None] = None, per: Union[str, None] = None,current_user: User = Depends(get_current_user)):
    if id and per:
        data = get_data.getDataInMongo(id, per)
        return data
    return {'error':'no data'}