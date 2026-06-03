from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.assessment_subcategory import (
    AssessmentSubcategory as AssessmentSubcategoryModel
)

from app.schemas.assessment_subcategory import (
    AssessmentSubcategoryCreate
)

router = APIRouter()


@router.get("/")
def get_subcategories(
    db: Session = Depends(get_db)
):
    return db.query(
        AssessmentSubcategoryModel
    ).all()


@router.post("/")
def create_subcategory(
    subcategory: AssessmentSubcategoryCreate,
    db: Session = Depends(get_db)
):

    new_subcategory = AssessmentSubcategoryModel(
        category_id=subcategory.category_id,
        name=subcategory.name,
        description=subcategory.description,
        display_order=subcategory.display_order,
        is_active=subcategory.is_active
    )

    db.add(new_subcategory)

    db.commit()

    db.refresh(new_subcategory)

    return new_subcategory


@router.put("/{id}")
def update_subcategory(
    id: int,
    subcategory: AssessmentSubcategoryCreate,
    db: Session = Depends(get_db)
):

    existing_subcategory = db.query(
        AssessmentSubcategoryModel
    ).filter(
        AssessmentSubcategoryModel.id == id
    ).first()

    if not existing_subcategory:

        raise HTTPException(
            status_code=404,
            detail="Subcategory not found"
        )

    existing_subcategory.category_id = subcategory.category_id
    existing_subcategory.name = subcategory.name
    existing_subcategory.description = subcategory.description
    existing_subcategory.display_order = subcategory.display_order
    existing_subcategory.is_active = subcategory.is_active

    db.commit()

    db.refresh(existing_subcategory)

    return existing_subcategory


@router.delete("/{id}")
def delete_subcategory(
    id: int,
    db: Session = Depends(get_db)
):

    subcategory = db.query(
        AssessmentSubcategoryModel
    ).filter(
        AssessmentSubcategoryModel.id == id
    ).first()

    if not subcategory:

        raise HTTPException(
            status_code=404,
            detail="Subcategory not found"
        )

    db.delete(subcategory)

    db.commit()

    return {
        "message": "Subcategory deleted"
    }