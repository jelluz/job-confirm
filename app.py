from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
# from sqladmin import Admin, ModelView
from starlette_admin.contrib.sqlmodel import Admin, ModelView

from starlette_admin import (
    CollectionField,
    ColorField,
    EmailField,
    ExportType,
    IntegerField,
    JSONField,
    ListField,
    StringField,
    URLField,
)
from sqlalchemy import Column, Text

from fastapi import FastAPI


class Outage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str = Field(max_length=2000)
    content: str = Field(sa_column=Column(Text))


# class OutageAdmin(ModelView, model=Outage):
#     column_list = [Outage.id, Outage.title, Outage.description]



sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


class MyModelView(ModelView):
    pass
    # page_size = 5
    # page_size_options = [5, 10, 25 - 1]
    # export_types = [ExportType.EXCEL, ExportType.CSV]


app = FastAPI()
admin = Admin(engine)
admin.add_view(MyModelView(Outage))
# admin.add_view(OutageAdmin)
admin.mount_to(app)


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
