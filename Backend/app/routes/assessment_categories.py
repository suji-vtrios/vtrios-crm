from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.assessment_category import (
    AssessmentCategory as AssessmentCategoryModel
)

from app.schemas.assessment_category import (
    AssessmentCategoryCreate,
    AssessmentCategory
)

router = APIRouter()


@router.get("/")
def get_categories(
    db: Session = Depends(get_db)
):
    return db.query(
        AssessmentCategoryModel
    ).all()


@router.post("/")
def create_category(
    category: AssessmentCategoryCreate,
    db: Session = Depends(get_db)
):

    existing_category = db.query(
        AssessmentCategoryModel
    ).filter(
        AssessmentCategoryModel.name
        == category.name
    ).first()

    if existing_category:

        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    new_category = AssessmentCategoryModel(
        name=category.name,
        description=category.description,
        display_order=category.display_order,
        is_active=category.is_active
    )

    db.add(new_category)

    db.commit()

    db.refresh(new_category)

    return new_category


@router.put("/{id}")
def update_category(
    id: int,
    category: AssessmentCategoryCreate,
    db: Session = Depends(get_db)
):

    existing_category = db.query(
        AssessmentCategoryModel
    ).filter(
        AssessmentCategoryModel.id == id
    ).first()

    if not existing_category:

        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    existing_category.name = category.name
    existing_category.description = category.description
    existing_category.display_order = category.display_order
    existing_category.is_active = category.is_active

    db.commit()

    db.refresh(existing_category)

    return existing_category


@router.delete("/{id}")
def delete_category(
    id: int,
    db: Session = Depends(get_db)
):

    category = db.query(
        AssessmentCategoryModel
    ).filter(
        AssessmentCategoryModel.id == id
    ).first()

    if not category:

        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    db.delete(category)

    db.commit()

    return {
        "message": "Category deleted"
    }