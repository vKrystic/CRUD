from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import models, schemas
from datetime import datetime

def create(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(
        customer_name=order.customer_name,
        description=order.description,
        order_date=datetime.now()  # Set to the current date and time
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def read_all(db: Session):
    return db.query(models.Order).all()

def read_one(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

def update(db: Session, order_id: int, order: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    update_data = order.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)
    return db_order

def delete(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    db.delete(db_order)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)