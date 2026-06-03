from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.assessment_competency import (
    AssessmentCompetency as AssessmentCompetencyModel
)

from app.schemas.assessment_competency import (
    AssessmentCompetencyCreate
)

router = APIRouter()


@router.get("/")
def get_competencies(
    db: Session = Depends(get_db)
):
    return db.query(
        AssessmentCompetencyModel
    ).all()


@router.post("/")
def create_competency(
    competency: AssessmentCompetencyCreate,
    db: Session = Depends(get_db)
):

    new_competency = AssessmentCompetencyModel(
        subcategory_id=competency.subcategory_id,
        name=competency.name,
        description=competency.description,
        weight=competency.weight,
        is_active=competency.is_active
    )

    db.add(new_competency)

    db.commit()

    db.refresh(new_competency)

    return new_competency


@router.put("/{id}")
def update_competency(
    id: int,
    competency: AssessmentCompetencyCreate,
    db: Session = Depends(get_db)
):

    existing_competency = db.query(
        AssessmentCompetencyModel
    ).filter(
        AssessmentCompetencyModel.id == id
    ).first()

    if not existing_competency:

        raise HTTPException(
            status_code=404,
            detail="Competency not found"
        )

    existing_competency.subcategory_id = competency.subcategory_id
    existing_competency.name = competency.name
    existing_competency.description = competency.description
    existing_competency.weight = competency.weight
    existing_competency.is_active = competency.is_active

    db.commit()

    db.refresh(existing_competency)

    return existing_competency


@router.delete("/{id}")
def delete_competency(
    id: int,
    db: Session = Depends(get_db)
):

    competency = db.query(
        AssessmentCompetencyModel
    ).filter(
        AssessmentCompetencyModel.id == id
    ).first()

    if not competency:

        raise HTTPException(
            status_code=404,
            detail="Competency not found"
        )

    db.delete(competency)

    db.commit()

    return {
        "message": "Competency deleted"
    }