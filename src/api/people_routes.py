from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Optional
from sqlalchemy.orm import Session
from src.db.repositories.people_repository import PeopleRepository
from src.schemas.people import PeopleCreate, PeopleOut, PeopleUpdate
from src.db import get_db

people_api_router = APIRouter(prefix="/people")


@people_api_router.post("/create", response_model=Dict, status_code=status.HTTP_201_CREATED)
def create_person(person: PeopleCreate, db: Session = Depends(get_db)):
    people_repo = PeopleRepository(db)
    created_person = people_repo.create_person(person)
    return {
        "status": "success",
        "message": f"Person with ID {created_person.id} created successfully.",
        "data": created_person.dict()
    }


@people_api_router.get("/{person_id}", response_model=Dict)
def get_person(person_id: int, db: Session = Depends(get_db)):
    people_repo = PeopleRepository(db)
    person = people_repo.get_person_by_id(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return {
        "status": "success",
        "message": f"Person with ID {person_id} retrieved successfully.",
        "data": person.dict()
    }


@people_api_router.get("/", response_model=Dict)
def get_all_people(db: Session = Depends(get_db)):
    people_repo = PeopleRepository(db)
    people = people_repo.get_all_people()
    return {
        "status": "success",
        "message": "All people retrieved successfully.",
        "data": [person.dict() for person in people]
    }


@people_api_router.patch("/update/{person_id}", response_model=Dict)
def update_person(person_id: int, person_data: PeopleUpdate, db: Session = Depends(get_db)):
    people_repo = PeopleRepository(db)
    updated_person = people_repo.update_person(person_id, person_data)
    if not updated_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return {
        "status": "success",
        "message": f"Person with ID {person_id} updated successfully.",
        "data": updated_person.dict()
    }


@people_api_router.delete("/delete/{person_id}", response_model=Optional[Dict])
def delete_person(person_id: int, db: Session = Depends(get_db)):
    people_repo = PeopleRepository(db)
    deleted_person_id = people_repo.delete_person_by_id(person_id)
    if not deleted_person_id:
        raise HTTP
