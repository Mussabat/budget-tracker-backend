from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from app.database import get_db
from app.models.models import Transaction, Subcategory, Category
from app.schemas.schemas import TransactionCreate, TransactionUpdate, TransactionResponse
from datetime import date

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@router.post("/", response_model=TransactionResponse)
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)):
    subcategory = db.query(Subcategory).filter(Subcategory.id == payload.subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    transaction = Transaction(**payload.dict())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

@router.get("/subcategory/{subcategory_id}", response_model=list[TransactionResponse])
def get_transactions_by_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    subcategory = db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    today = date.today()
    return db.query(Transaction)\
        .filter(Transaction.subcategory_id == subcategory_id)\
        .filter(extract("year", Transaction.date) == today.year)\
        .filter(extract("month", Transaction.date) == today.month)\
        .order_by(Transaction.date.desc()).all()

@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(transaction_id: int, payload: TransactionUpdate, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    transaction.amount = payload.amount
    transaction.date = payload.date
    db.commit()
    db.refresh(transaction)
    return transaction

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return {"detail": "Transaction deleted"}

@router.get("/summary/{category_id}", response_model=dict)
def get_monthly_summary(category_id: int, month: str, db: Session = Depends(get_db)):
    # month format: "2026-05"
    year, mon = map(int, month.split("-"))
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    total_spent = db.query(func.sum(Transaction.amount))\
        .join(Subcategory)\
        .filter(Subcategory.category_id == category_id)\
        .filter(extract("year", Transaction.date) == year)\
        .filter(extract("month", Transaction.date) == mon)\
        .scalar() or 0.0

    return {
        "category": category.name,
        "budget_limit": category.budget_limit,
        "total_spent": round(total_spent, 2),
        "remaining": round(category.budget_limit - total_spent, 2),
        "is_over_budget": total_spent > category.budget_limit
    }

@router.get("/history", response_model=list[dict])
def get_monthly_history(month: str, db: Session = Depends(get_db)):
    year, mon = map(int, month.split("-"))

    categories = db.query(Category).all()
    history = []

    for category in categories:
        total_spent = db.query(func.sum(Transaction.amount))\
            .join(Subcategory)\
            .filter(Subcategory.category_id == category.id)\
            .filter(extract("year", Transaction.date) == year)\
            .filter(extract("month", Transaction.date) == mon)\
            .scalar() or 0.0

        history.append({
            "category": category.name,
            "budget_limit": category.budget_limit,
            "total_spent": round(total_spent, 2),
            "remaining": round(category.budget_limit - total_spent, 2),
            "is_over_budget": total_spent > category.budget_limit
        })

    return history