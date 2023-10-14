from models import Klus, Schoonmaker, Pand
# from sqladmin import Admin, ModelView
from starlette_admin.contrib.sqlmodel import Admin, ModelView
from sqlmodel import  SQLModel, create_engine, Session, select

from fastapi import FastAPI


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()
admin = Admin(engine)

admin.add_view(ModelView(Klus))
admin.add_view(ModelView(Schoonmaker))
admin.add_view(ModelView(Pand))
admin.mount_to(app)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

@app.post("/klussen/")
def create_outage(klus: Klus):
    with Session(engine) as session:
        session.add(klus)
        session.commit()
        session.refresh(klus)
        return klus
    

@app.get("/klussen/")
def read_heroes():
    with Session(engine) as session:
        klussen = session.exec(select(Klus)).all()
        return klussen
        

@app.get("/")
async def root():
    return {"message": "Hello World"}

