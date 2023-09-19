from sqlmodel import Field, SQLModel, Column, Text, Relationship
from pydantic import EmailStr


class Schoonmaker(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    naam: str = Field(index=True)
    email: EmailStr = Field(index=True)
    klussen: list["Klus"] | None = Relationship(back_populates="schoonmaker")



class Pand(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    naam: str = Field(index=True)
    adres: str = Field()
    # klussen: list["Klus"] | None = Relationship(back_populates="pand")


class Klus(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    titel: str = Field(index=True)
    beschrijving: str = Field(sa_column=Column(Text))
    # team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    schoonmaker_id: int | None= Field(default=None, foreign_key="schoonmaker.id")
    schoonmaker: Schoonmaker = Relationship(back_populates="klussen")
    pand_id: int|None = Field(default=None, foreign_key="pand.id")
    # pand: Pand = Relationship(back_populates="klussen")