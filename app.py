from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

from fastapi import FastAPI


class Outage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/outage/")
def create_outage(outage: Outage):
    with Session(engine) as session:
        session.add(outage)
        session.commit()
        session.refresh(outage)
        return outage
    

@app.get("/outage/")
def read_heroes():
    with Session(engine) as session:
        outage = session.exec(select(Outage)).all()
        return outage
        

@app.get("/")
async def root():
    return {"message": "Hello World"}
