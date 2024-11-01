from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List, Optional
from src.db.models import People
from src.schemas.people import PeopleCreate, PeopleOut, PeopleUpdate


class PeopleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_person(self, person: PeopleCreate) -> PeopleOut:
        db_person = People(**person.dict())
        self.db.add(db_person)
        self.db.commit()
        self.db.refresh(db_person)
        return P eopleOut.from_orm(db_person)

    def get_person_by_id(self, person_id: int) -> Optional[PeopleOut]:
        try:
            db_person = self.db.query(People).filter(People.id == person_id).one()
            return PeopleOut.from_orm(db_person)
        except NoResultFound:
            return None

    def get_all_people(self) -> List[PeopleOut]:
        db_people = self.db.query(People).all()
        return [PeopleOut.from_orm(person) for person in db_people]

    def update_person(self, person_id: int, person_data: PeopleUpdate) -> Optional[PeopleOut]:
        db_person = self.db.query(People).filter(People.id == person_id).first()
        if not db_person:
            return None
        for field, value in person_data.dict(exclude_unset=True).items():
            setattr(db_person, field, value)
        self.db.commit()
        self.db.refresh(db_person)
        return PeopleOut.from_orm(db_person)

    def delete_person_by_id(self, person_id: int) -> Optional[int]:
        db_person = self.db.query(People).filter(People.id == person_id).first()
        if db_person:
            self.db.delete(db_person)
            self.db.commit()
            return person_id
        return None
