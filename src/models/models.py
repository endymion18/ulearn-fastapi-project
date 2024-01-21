from typing import Type

from sqlalchemy import Identity, Integer, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class MainPage(Base):
    __tablename__ = 'main_page'

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    value: Mapped[str] = mapped_column(String(length=10), nullable=False)
    vacancy_name: Mapped[str] = mapped_column(String(length=30), nullable=False)
    first_paragraph: Mapped[str] = mapped_column(String(length=3000), nullable=False)
    second_paragraph_name: Mapped[str] = mapped_column(String(length=30), nullable=False)
    second_paragraph: Mapped[str] = mapped_column(String(length=3000), nullable=False)
    img_paths: Mapped[Type] = mapped_column(JSON)


