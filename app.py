from models import Job, Contractor, Location
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

admin.add_view(ModelView(Job))
admin.add_view(ModelView(Contractor))
admin.add_view(ModelView(Location))
admin.mount_to(app)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

@app.post("/jobs/")
def create_outage(job: Job):
    with Session(engine) as session:
        session.add(job)
        session.commit()
        session.refresh(job)
        return job
    

@app.get("/jobs/")
def read_heroes():
    with Session(engine) as session:
        jobsen = session.exec(select(Job)).all()
        return jobsen
        

@app.get("/")
async def root():
    return {"message": "Hello World"}

