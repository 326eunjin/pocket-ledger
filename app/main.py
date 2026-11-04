from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import Base, get_session, make_engine
from app.models import Expense
from app.schemas import ExpenseCreate, ExpenseRead

DbSession = Annotated[Session, Depends(get_session)]


def create_app(database_url: str = "sqlite:///./pocket_ledger.db") -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI):
        engine = make_engine(database_url)
        application.state.engine = engine
        try:
            Base.metadata.create_all(engine)
            yield
        finally:
            engine.dispose()

    application = FastAPI(title="PocketLedger", lifespan=lifespan)

    @application.post(
        "/expenses", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED
    )
    def create_expense(payload: ExpenseCreate, session: DbSession):
        values = payload.model_dump(exclude={"amount"})
        expense = Expense(**values, amount_cents=int(payload.amount * 100))
        try:
            session.add(expense)
            session.commit()
            session.refresh(expense)
        except SQLAlchemyError:
            session.rollback()
            raise HTTPException(status_code=500, detail="Unable to save expense") from None
        return expense

    @application.get("/expenses", response_model=list[ExpenseRead])
    def list_expenses(
        session: DbSession,
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 100,
    ):
        return session.scalars(
            select(Expense).order_by(Expense.id).offset(offset).limit(limit)
        ).all()

    @application.get("/expenses/{expense_id}", response_model=ExpenseRead)
    def get_expense(expense_id: int, session: DbSession):
        expense = session.get(Expense, expense_id)
        if expense is None:
            raise HTTPException(status_code=404, detail="Expense not found")
        return expense

    return application


app = create_app()
