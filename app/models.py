from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Expense(Base):
    __tablename__ = "expenses"
    __table_args__ = (CheckConstraint("amount_cents > 0"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    amount_cents: Mapped[int]
    category: Mapped[str]
    description: Mapped[str]
    expense_date: Mapped[date]
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )

    @property
    def amount(self) -> Decimal:
        return (Decimal(self.amount_cents) / 100).quantize(Decimal("0.01"))
