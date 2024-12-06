from typing import Union

from fastapi import FastAPI
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.sql.annotation import Annotated
from sqlmodel import Field, SQLModel, create_engine, Session

app = FastAPI()

DATABASE_URL = "mysql+pymysql://root:admin@localhost:3306/universities_info_db"


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class University(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=250)
    page_url: str = Field(max_length=250)


class Carrer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=250)
    page_url: str = Field(max_length=250)
    price: float
    university_id: int = Field(foreign_key="university.id")


class Subject(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=250)
    file_url: str = Field(max_length=250)
    semester: int
    carrer_id: int = Field(foreign_key="carrer.id")

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
