from sqlmodel import Field, SQLModel, Column, Text, Relationship
from pydantic import EmailStr
from starlette.requests import Request
from datetime import datetime
from sqlalchemy import DateTime

class Contractor(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: EmailStr = Field(index=True)
    jobs: list["Job"] | None = Relationship(back_populates="contractor")
    telephone: str|None = Field()

    async def __admin_repr__(self, request: Request):
        return self.name   



class Location(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    address: str = Field()
    jobs: list["Job"] | None = Relationship(back_populates="location")

    async def __admin_repr__(self, request: Request):
        return self.name
    

class Job(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str = Field(sa_column=Column(Text))
    created: datetime | None = Field(
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow)
    )
    solved: bool = Field(default=False)

    # team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    contractor_id: int | None = Field(default=None, foreign_key="contractor.id")
    contractor: Contractor = Relationship(back_populates="jobs")
    location_id: int | None = Field(default=None, foreign_key="location.id")
    location: Location = Relationship(back_populates="jobs")
