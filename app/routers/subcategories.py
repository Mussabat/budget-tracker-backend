from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Subcategory, Transaction
from app.schemas.schemas import SubcategoryCreate, SubcategoryResponse, SubcategoryUpdate

router = APIRouter(
    prefix="/subcategories",
    tags=["Subcategories"]
)

@router.get("/{category_id}", response_model=list[SubcategoryResponse])
def get_subcategories(category_id: int, db: Session = Depends(get_db)):
    subcategories = db.query(Subcategory).filter(Subcategory.category_id == category_id).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "category_id": s.category_id,
            "total_spent": sum(t.amount for t in s.transactions),
        }
        for s in subcategories
    ]

@router.post("/", response_model=SubcategoryResponse)
def create_subcategory(payload: SubcategoryCreate, db: Session = Depends(get_db)):
    subcategory = Subcategory(**payload.dict())
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)
    return subcategory

@router.put("/{subcategory_id}", response_model=SubcategoryResponse)
def update_subcategory(subcategory_id: int, payload: SubcategoryUpdate, db: Session = Depends(get_db)):
    subcategory = db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    subcategory.name = payload.name
    db.commit()
    db.refr