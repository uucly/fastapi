import logging
import secrets
from typing import Optional

import graphene as graphene
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from singleton.singleton import Singleton
from sqlalchemy.orm import Session
from starlette import status
from starlette.graphql import GraphQLApp

from MyService import MyService
from sql_app import crud, models
from sql_app.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

security = HTTPBasic()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/oauth/items")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "sven")
    correct_password = secrets.compare_digest(credentials.password, "mysecret")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/users/other")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/items/service/{item_id}")
def read_from_serviceitem(item_id: int, q: Optional[str] = None, my_service: MyService = Depends(MyService)):
    return my_service.get_infos(item_id=item_id, q=q)


@app.get("/items/db/{marker_id}")
def read_item_from_db(marker_id: int, db: Session = Depends(get_db)) -> models.Marker:
    return crud.get_marker(db=db, marker_id=marker_id)


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        print(info)
        # logging.Logger.info(info)
        return "Hello " + name


app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
