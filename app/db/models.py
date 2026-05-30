from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    members = relationship("EventMember", backref="event")
    expenses = relationship("Expense", backref="event")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    payer_id = Column(Integer, ForeignKey("event_members.id"), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    splits = relationship("ExpenseSplit", backref="expense")


class EventMember(Base):
    __tablename__ = "event_members"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # имя внутри события (важно!)
    display_name = Column(String, nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User")
    expenses_paid = relationship("Expense", backref="payer")

    __table_args__ = (
        UniqueConstraint("event_id", "display_name", name="uq_event_display_name"),
    )


class ExpenseSplit(Base):
    __tablename__ = "expense_splits"

    id = Column(Integer, primary_key=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("event_members.id"), nullable=False)
    amount = Column(Float, nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("expense_id", "member_id", name="uq_expense_member"),
    )    
